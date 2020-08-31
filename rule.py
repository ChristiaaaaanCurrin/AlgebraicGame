from abc import abstractmethod, ABC
from game_state import GameState


class Rule(ABC):
    def __init__(self, max_iteration=1):
        self.max_iteration = max_iteration

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

    def does_decorate(self, state, move):
        return True

    def legal(self, state, move):
        return move in self.get_legal_moves(state)

    @abstractmethod
    def state_requirements(self):
        return {}

    @abstractmethod
    def get_legal_moves(self, state):
        pass

    @abstractmethod
    def execute_move(self, state, move):
        pass

    @abstractmethod
    def undo_move(self, state, move):
        pass


class Pass(Rule):
    def __init__(self, val="Pass", **kwargs):
        self.val = val
        super().__init__(**kwargs)

    def __repr__(self):
        return self.val.__repr__()

    def __str__(self):
        return self.val.__str__()

    def state_requirements(self):
        return {}

    def get_legal_moves(self, state):
        return [self.val]

    def execute_move(self, state, move):
        if move == self.val:
            return state
        else:
            return False

    def undo_move(self, state, move):
        if move == self.val:
            return state
        else:
            return False


class ZeroRule(Rule):
    def __repr__(self):
        return 'ZERO'

    def state_requirements(self):
        return {}

    def get_legal_moves(self, state):
        return []

    def execute_move(self, state, move):
        return False

    def undo_move(self, state, move):
        return False


class RuleSum(Rule):
    def __init__(self, *rules, **kwargs):
        self.sub_rules = rules
        super().__init__(**kwargs)

    def __repr__(self):
        return '(' + ' + '.join([rule.__repr__() for rule in self.sub_rules]) + ')'

    def __str__(self):
        return '(' + ' + '.join([rule.__str__() for rule in self.sub_rules]) + ')'

    def state_requirements(self):
        requirements = {}
        for rule in self.sub_rules:
            requirements.update(rule.state_requirements())
        return requirements

    def legal(self, state, move):
        for rule in self.sub_rules:
            if rule.legal(state, move):
                return True
        else:
            return False

    def get_legal_moves(self, state):
        legal = []
        for rule in self.sub_rules:
            for move in rule.get_legal_moves(state):
                legal.append(move)
        return legal

    def execute_move(self, state, move):
        for rule in self.sub_rules:
            new_state = rule.execute_move(move, state)
            if new_state:
                return new_state
        else:
            return False

    def undo_move(self, state, move):
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
        return f'({self.positive} - {self.negative})'

    def state_requirements(self):
        return {**self.positive.state_requirements(), **self.negative.state_requirements()}

    def get_legal_moves(self, state):
        return filter(lambda m: not self.negative.legal(state, m), self.positive.get_legal_moves(state))

    def execute_move(self, state, move):
        return self.positive.execute_move(state, move)

    def undo_move(self, state, move):
        return self.positive.undo_move(state, state)


class RuleProduct(Rule):
    def __init__(self, *rules, blocking=True, **kwargs):
        self.sub_rules = rules
        self.blocking = blocking
        super().__init__(**kwargs)

    def __repr__(self):
        return ' * '.join([rule.__repr__() for rule in self.sub_rules])

    def __str__(self):
        return ' * '.join([rule.__str__() for rule in self.sub_rules])

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
                    if rule.does_decorate(state, (move2, *move1)):
                        new_legal.append((move2, *move1))
            legal = new_legal
        return legal

    def execute_move(self, state, move):
        rules = self.sub_rules
        while move and rules and state:
            *move, comp = move
            *rules, rule = rules
            new_state = rule.execute_move(state, comp)
            state = new_state if (self.blocking or new_state) else state
        return state

    def undo_move(self, state, move):
        rules = self.sub_rules
        while move and rules and state:
            *move, comp = move
            *rules, rule = rules
            state = rule.undo_move(state, comp)
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
