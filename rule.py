from abc import abstractmethod, ABC
from game_state import GameState


class Rule(ABC):
    def __init__(self, listable, **kwargs):
        self.listable = listable
        self.iterate = 1

    def __iter__(self):
        self.iterate = 1
        return self

    def __next__(self):
        if self.iterate:
            self.iterate -= 1
            return self
        else:
            raise StopIteration

    def __and__(self, other):
        if self.listable:
            return ListRuleAnd(self, other)
        elif other.listable:
            return other & self
        else:
            return FuncRuleAnd(self, other)

    def __or__(self, other):
        if not other.listable:
            return FuncRuleOr(self, other)
        elif not self.listable:
            return other | self
        else:
            return ListRuleOr(self, other)

    def __invert__(self):
        return NotRule(self)

    def __mul__(self, other):
        return RuleProduct(self, other)

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


# The Two Kinds of Rules

class FuncRule(Rule, ABC):
    def __init__(self, **kwargs):
        super().__init__(False, **kwargs)

    def get_legal_moves(self, state):
        return NotImplemented


class ListRule(Rule, ABC):
    def __init__(self, **kwargs):
        super().__init__(listable=True, **kwargs)

    def legal(self, state, move):
        return move in self.get_legal_moves(state)


# Combination Rules

class RuleCombination(Rule, ABC):
    def __init__(self, *rules, **kwargs):
        super().__init__(**kwargs)
        self.sub_rules = rules

    def __iter__(self):
        return iter(self.sub_rules)

    def __next__(self):
        return next(self.sub_rules)

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


class FuncRuleAnd(RuleCombination, FuncRule):
    LISTABLE = False

    def legal(self, state, move):
        return all(map(lambda r: r.legal(state, move), self.sub_rules))


class ListRuleAnd(RuleCombination, ListRule):
    LISTABLE = True

    def get_legal_moves(self, state):
        rule, *rules = self.sub_rules
        legal = rule.get_legal_moves(state)
        while rules:
            rule, *rules = rules
            legal = filter(lambda m: rule.legal(state, m), legal)
        return legal


class FuncRuleOr(RuleCombination, FuncRule):
    LISTABLE = False

    def legal(self, state, move):
        return any(map(lambda r: r.legal(state, move), self.sub_rules))


class ListRuleOr(RuleCombination, ListRule):
    LISTABLE = True

    def get_legal_moves(self, state):
        legal = []
        [legal.extend(rule.get_legal_moves(state)) for rule in self.sub_rules]
        return legal


class NotRule(FuncRule):
    LISTABLE = False

    def __init__(self, rule, **kwargs):
        self.rule = rule
        super().__init__(**kwargs)

    def legal(self, state, move):
        return not self.rule.legal(state, move)

    def state_requirements(self):
        return self.rule.state_requirements()

    def execute_move(self, state, move):
        return self.rule.execute_move()

    def undo_move(self, state, move):
        return self.rule.execute_move()


class RuleProduct(RuleCombination, ListRule):
    LISTABLE = True

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


# Basic Rules

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
    c = Pass('c')
    aMinus = ~a
    allow = AllowAny()
    zero = ZeroRule()
    two = (b & ~c)
    four = two | two
    [print(list(num.get_legal_moves("any"))) for num in (zero, a, b, two, four)]
    print(two.execute_move('any', 'b'))
