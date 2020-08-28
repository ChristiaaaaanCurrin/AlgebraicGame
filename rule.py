from abc import abstractmethod, ABC
from game_state import GameState


class Rule(ABC):
    def __init__(self, **kwargs):
        kwargs = {"max_iteration": 1, **kwargs}
        self.max_iteration = kwargs.pop('max_iteration')
        assert kwargs == {}, "unexpected arguments: " + str(kwargs)

    def __iter__(self):
        self.max_iteration = 1
        return self

    def __next__(self):
        if self.max_iteration:
            self.max_iteration -= 1
            return self
        else:
            raise StopIteration

    def __add__(self, other):
        return RuleSum(self, other)

    def __sub__(self, other):
        return SubtractRule(self, other)

    def __mul__(self, other):
        return RuleProduct(*self, *other)

    def __pow__(self, other):
        return RuleProduct(self, other)

    def create_state(self, **kwargs):
        return GameState(self, **{**self.state_requirements(), **kwargs})

    def does_decorate(self, *move, state):
        return True

    def legal(self, move, state):
        return move in self.get_legal_moves(state)

    def flatten(self):
        return [self]

    @abstractmethod
    def state_requirements(self):
        return {}

    @abstractmethod
    def get_legal_moves(self, state):
        pass

    @abstractmethod
    def execute_move(self, move, state):
        pass

    @abstractmethod
    def undo_move(self, move, state):
        pass


class Pass(Rule):
    def __init__(self, val="Pass", **kwargs):
        self.val = val
        super().__init__(**kwargs)

    def __repr__(self):
        return self.val.__repr__()

    def state_requirements(self):
        return {}

    def get_legal_moves(self, state):
        return [self.val]

    def execute_move(self, move, state):
        if move == self.val:
            return state
        else:
            return False

    def undo_move(self, move, state):
        if move == self.val:
            return state
        else:
            return False


class ZeroRule(Rule):
    def state_requirements(self):
        return {}

    def get_legal_moves(self, state):
        return []

    def execute_move(self, move, state):
        return False

    def undo_move(self, move, state):
        return False


class RuleSum(Rule):
    def __init__(self, *rules, **kwargs):
        self.sub_rules = rules
        super().__init__(**kwargs)

    def __repr__(self):
        sub_string = ""
        for rule in self.sub_rules:
            sub_string = sub_string + str(rule) + ' + '
        return '(' + sub_string[:-3] + ')'

    def flatten(self):
        flat = []
        for rule in self.sub_rules:
            flat.extend(rule.flatten())
        return flat

    def state_requirements(self):
        requirements = {}
        for rule in self.sub_rules:
            requirements.update(rule.state_requirements())
        return requirements

    def get_legal_moves(self, state):
        legal = []
        for rule in self.sub_rules:
            for move in rule.get_legal_moves(state):
                legal.append(move)
        return legal

    def execute_move(self, move, state):
        for rule in self.sub_rules:
            new_state = rule.execute_move(move, state)
            if new_state:
                return new_state
        else:
            return False

    def undo_move(self, move, state):
        for rule in self.sub_rules:
            new_state = rule.undo_move(move, state)
            if new_state:
                return new_state
        else:
            return False


class SubtractRule(Rule):
    def __init__(self, pos, neg, **kwargs):
        self.positive = pos
        self.negative = neg
        super().__init__(**kwargs)

    def __repr__(self):
        return '(' + str(self.positive) + ' - ' + str(self.negative) + ')'

    def state_requirements(self):
        return {**self.positive.state_requirements(), **self.negative.state_requirements()}

    def get_legal_moves(self, state):
        legal = filter(lambda m: not self.negative.legal(m, state), self.positive.get_legal_moves(state))
        return legal

    def execute_move(self, move, state):
        return self.positive.execute_move(move, state)

    def undo_move(self, move, state):
        return self.positive.undo_move(move, state)


class RuleProduct(Rule):
    def __init__(self, *rules, blocking=True, **kwargs):
        self.sub_rules = rules
        self.blocking = blocking
        super().__init__(**kwargs)

    def __repr__(self):
        sub_string = ""
        joiner = ' * ' if self.blocking else ' *>'
        for rule in self.sub_rules:
            sub_string = sub_string + str(rule) + joiner
        return sub_string[:-3]

    def __iter__(self):
        return iter(self.sub_rules)

    def __next__(self):
        return next(self.sub_rules)

    def state_requirements(self):
        requirements = {}
        for rule in self.sub_rules:
            requirements.update(**rule.state_requirements())
        return requirements

    def get_legal_moves(self, state):
        legal = [()]
        rules = self.sub_rules
        while rules:
            new_legal = []
            *rules, rule = rules
            for move1 in legal:
                for move2 in rule.get_legal_moves(state):
                    if rule.does_decorate(move2, *move1, state=state):
                        new_legal.append((move2, *move1))
            legal = new_legal
        return legal

    def execute_move(self, move, state):
        rules = self.sub_rules
        while move and rules and state:
            *move, comp = move
            *rules, rule = rules
            new_state = rule.execute_move(comp, state)
            state = new_state if (self.blocking or new_state) else state
        return state

    def undo_move(self, move, state):
        rules = self.sub_rules
        while move and rules and state:
            *move, comp = move
            *rules, rule = rules
            state = rule.undo_move(comp, state)
        return state


if __name__ == "__main__":
    one = Pass()
    zero = ZeroRule()
    two = one + one
    four = two * zero + one
    [print(num.get_legal_moves("any")) for num in (zero, one, two, four)]
    print(two.execute_move('ID', 'any'))
    print(list(one))
    print(four)
