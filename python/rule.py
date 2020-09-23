from abc import abstractmethod, ABC
from python.game_state import GameState


class Rule(ABC):
    def __and__(self, other):
        return RuleAnd(self, other)

    def __or__(self, other):
        return RuleOr(self, other)

    def __mul__(self, other):
        return RuleIndependentProduct(self, other)

    def __pow__(self, power, modulo=None):
        return RuleDependentProduct(self, power)

    def __sub__(self, other):
        return RuleSubtraction(self, other)

    def __invert__(self):
        return NotRule(self)

    def __call__(self, *args, **kwargs):
        return self.get_legal_moves(*args, **kwargs)

    def create_state(self, **kwargs):
        return GameState(self, **{**self.state_requirements(), **kwargs})

    @abstractmethod
    def state_requirements(self):
        pass

    @abstractmethod
    def get_legal_moves(self, state):
        pass

    @abstractmethod
    def execute_move(self, state, move):
        pass

    @abstractmethod
    def undo_move(self, state, move):
        pass


# -- Rule Combinations ------------------------------------

class RuleCombination(Rule, ABC):

    operator = ' combined with '

    def __init__(self, *rules, **kwargs):
        self.sub_rules = rules
        super().__init__(**kwargs)

    def __iter__(self):
        return iter(self.sub_rules)

    def __next__(self):
        return next(self.sub_rules)

    def __repr__(self):
        return f"({self.operator.join([rule.__repr__() for rule in self.sub_rules])})"

    def __str__(self):
        return f"({self.operator.join([rule.__str__() for rule in self.sub_rules])})"

    def state_requirements(self):
        requirements = {}
        [requirements.update(rule.state_requirements()) for rule in self.sub_rules]
        return requirements

    def execute_move(self, state, move):
        for rule in self.sub_rules:
            new_state = rule.execute_move(state, move)
            if new_state:
                return new_state
        else:
            return False

    def undo_move(self, state, move):
        for rule in self.sub_rules:
            new_state = rule.undo_move(state, move)
            if new_state:
                return new_state
        else:
            return False


class RuleAnd(RuleCombination):
    operator = ' & '

    def get_legal_moves(self, state):
        rule, *rules = self.sub_rules
        legal = rule.get_legal_moves(state)
        for rule in rules:
            legal = filter(lambda m: m in rule.get_legal_moves(state), legal)
        return legal


class RuleOr(RuleCombination):
    operator = ' | '

    def get_legal_moves(self, state):
        legal = []
        [legal.extend(rule.get_legal_moves(state)) for rule in self.sub_rules]
        return legal


class NotRule(Rule):
    def __init__(self, rule, **kwargs):
        self.rule = rule
        super().__init__(**kwargs)

    def __repr__(self):
        return '~' + self.rule.__repr__()

    def __str__(self):
        return '~' + self.rule.__str__()

    def state_requirements(self):
        return self.rule.state_requirements()

    def get_legal_moves(self, state):
        return [] if self.rule.legal(state) else [state]

    def execute_move(self, state, move):
        return self.rule.execute_move()

    def undo_move(self, state, move):
        return self.rule.execute_move()


class RuleSubtraction(RuleCombination):
    operator = ' - '

    def get_legal_moves(self, state):
        rule, *rules = self.sub_rules
        legal = rule.get_legal_moves(state)
        while rules:
            rule, *rules = rules
            legal = filter(lambda m: m not in rule.get_legal_moves(state), legal)
        return legal


class RuleIndependentProduct(RuleCombination):
    operator = ' * '

    def get_legal_moves(self, state):
        legal = [()]
        rules = self.sub_rules
        while rules:
            new_legal = []
            *rules, rule = rules
            for move1 in legal:
                for move2 in rule.get_legal_moves(state):
                    new_legal.append((move2, *move1))
            legal = new_legal
        return legal

    def execute_move(self, state, move):
        rules = self.sub_rules
        while move and rules and state:
            *move, comp = move
            *rules, rule = rules
            state = rule.execute_move(state, comp)
        return state

    def undo_move(self, state, move):
        rules = self.sub_rules
        while move and rules and state:
            comp, *move = move
            rule, *rules = rules
            state = rule.undo_move(state, comp)
        return state


class RuleDependentProduct(RuleIndependentProduct):
    operator = ' ** '

    def get_legal_moves(self, state):
        rule, *modifiers = self.sub_rules
        legal = []
        for move in rule.get_legal_moves(state):
            legal.append([move] + [modifier.legal(state, move) for modifier in modifiers])
        return legal


class RulePattern(RuleCombination):
    def __init__(self, step, start, stop, skip):
        self.step = step
        self.start = start
        self.stop = stop
        self.skip = skip
        super().__init__(self.step, self.start, self.stop, self.skip)

    def __repr__(self):
        return f'{self.step} |- {self.start}, {self.stop}, {self.skip}'

    def get_legal_moves(self, state):

        legal = self.start.get_legal_moves(state)
        edge = []
        [edge.extend(self.step.legal(state, move)) for move in legal]
        checked = []

        while edge:
            new_edge = []
            for move in edge:
                print(move)
                if not self.skip.legal(state, move) and move not in legal:
                    legal.append(move)
                if not self.stop.legal(state, move) and move not in checked:
                    new_edge.extend(self.step.legal(state, move))
                checked.append(move)
            edge = new_edge
        return legal


# -- Elementary Rules -------------------------------------

class ZeroRule(Rule):
    def __repr__(self):
        return 'ZeroRule'

    def get_legal_moves(self, state):
        return []

    def execute_move(self, state, move):
        return False

    def undo_move(self, state, move):
        return False

    def state_requirements(self):
        return {}


class ConstantRule(Rule):
    def __init__(self, value='Constant', **kwargs):
        self.value = value
        super().__init__(**kwargs)

    def __repr__(self):
        return str(self.value)

    def get_legal_moves(self, state):
        return [self.value]

    def execute_move(self, state, move):
        if move == self.value:
            return state
        else:
            return False

    def undo_move(self, state, move):
        if move == self.value:
            return state
        else:
            return False

    def state_requirements(self):
        return {}


class PassRule(Rule):
    def get_legal_moves(self, state):
        return [state]

    def state_requirements(self):
        return {}

    def execute_move(self, state, move):
        return False

    def undo_move(self, state, move):
        return False