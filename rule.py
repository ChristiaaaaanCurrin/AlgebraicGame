from abc import abstractmethod, ABC
from game_state import GameState


class Rule(ABC):
    def __init__(self, listable):
        self.listable = listable

    def __and__(self, other):
        if self.listable:
            attributes = {'get_legal_moves': lambda s: filter(lambda m: other.legal(s, m), self.get_legal_moves(s)),
                          'execute_move': lambda s, m: x if (x := self.execute_move(s, m)) else other.execute_move(s, m),
                          'undo_move': lambda s, m: x if (x := self.undo_move(s, m)) else other.undo_move(s, m)}
            return type('RuleAnd', (ListRule, object), attributes)

        elif other.listable:
            return other & self

        else:
            attributes = {'legal': lambda s, m: self.legal(s, m) and other.legal(s, m),
                          'execute_move': lambda s, m: self.execute_move(s, m),
                          'undo_move': lambda s, m: x if (x := self.undo_move(s, m)) else other.undo_move(s, m)}
            return type('RuleOr', (FuncRule, object), attributes)

    def __or__(self, other):
        if not other.listable:
            attributes = {'legal': lambda s, m: self.legal(s, m) or other.legal(s, m),
                          'execute_move': lambda s, m: x if (x := self.execute_move(s, m)) else other.execute_move(s, m),
                          'undo_move': lambda s, m: x if (x := self.undo_move(s, m)) else other.undo_move(s, m)}
            return type('RuleOr', (FuncRule, object), attributes)

        elif not self.listable:
            return other | self

        else:
            attributes = {'get_legal_moves': lambda s: self.get_legal_moves(s) + other.get_legal_moves(s),
                          'execute_move': lambda s, m: x if (x := self.execute_move(s, m)) else other.execute_move(s, m),
                          'undo_move': lambda s, m: x if (x := self.undo_move(s, m)) else other.undo_move(s, m)}
            return type('RuleOr', (ListRule, object), attributes)

    def create_state(self, **kwargs):
        return GameState(self, **{**self.state_requirements(), **kwargs})

    @abstractmethod
    def get_legal_moves(self, state):
        pass

    @abstractmethod
    def legal(self, state, move):
        pass

    @abstractmethod
    def state_requirements(self):
        pass

    @abstractmethod
    def execute_move(self, state, move):
        pass

    @abstractmethod
    def undo_move(self, state, move):
        pass


class FuncRule(Rule, ABC):
    def __init__(self):
        super().__init__(False)

    def get_legal_moves(self, state):
        pass

    @abstractmethod
    def legal(self, state, move):
        pass


class ListRule(Rule, ABC):
    def __init__(self, **kwargs):
        super().__init__(listable=True, **kwargs)

    @abstractmethod
    def get_legal_moves(self, state):
        pass

    def legal(self, state, move):
        return move in self.get_legal_moves(state)


class ZeroRule(Rule):
    def __init__(self):
        super().__init__(True)

    def legal(self, state, move):
        return False

    def get_legal_moves(self, state):
        return []

    def execute_move(self, state, move):
        return False

    def undo_move(self, state, move):
        return False

    def state_requirements(self):
        return {}


class Pass(Rule):
    def __init__(self, value='Pass'):
        self.value = value
        super().__init__(True)

    def legal(self, state, move):
        return move == self.value

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


class AllowAny(Pass):
    def __init__(self):
        super().__init__('Any')

    def legal(self, state, move):
        return True

    def get_legal_moves(self, state):
        return [1]

    def execute_move(self, state, move):
        return state

    def undo_move(self, state, move):
        return state


if __name__ == "__main__":
    a = Pass('a')
    b = Pass('b')
    allow = AllowAny()
    zero = ZeroRule()
    two = a | b
    four = two | two
    [print(list(num.get_legal_moves("any"))) for num in (zero, a, b, two)]
    print(two.execute_move('any', 'b'))
