from abc import ABC, abstractmethod
from move import Identity, SumMove, Composition, ParallelMove


class Rule(ABC):
    @abstractmethod
    def legal(self, state, move):
        pass

    def list_legal(self, state):
        return NotImplemented

    def __or__(self, other):
        return Union(self, other)

    def __and__(self, other):
        return Intersection(self, other)

    def __mul__(self, other):
        return CrossProduct(self, other)

    def __mod__(self, other):
        return DotProduct(self, other)

    def __add__(self, other):
        return self * PassRule() | PassRule() * other

    def graph(self, state):
        return [move(state) for move in self.list_legal(state)]


class VoidRule(Rule):
    def legal(self, state, move):
        return False

    def list_legal(self, state):
        return []

    def __repr__(self):
        return "0"

    def __or__(self, other):
        return other

    def __and__(self, other):
        return self

    def __mul__(self, other):
        return self

    def __mod__(self, other):
        return self


class PassRule(Rule):
    def __repr__(self):
        return "p"

    def legal(self, state, move):
        return move.get_inverse() == move

    def list_legal(self, state):
        return [Identity()]


class Union(Rule):
    def __init__(self, rule, *rules):
        self.children = (rule, *rules)

    def __repr__(self):
        return "(" + " | ".join([child.__repr__() for child in self.children]) + ")"

    def legal(self, state, move):
        for rule in self.children:
            if rule.legal(state, move):
                return True
        return False

    def list_legal(self, state):
        legal = []
        for rule in self.children:
            if rule.list_legal(state) == NotImplemented:
                return NotImplemented
            else:
                legal.extend(rule.list_legal(state))
        return legal


class Intersection(Rule):
    def __init__(self, rule, *rules):
        self.children = rule, *rules

    def __repr__(self):
        return "(" + " & ".join([child.__repr__() for child in self.children]) + ")"

    def legal(self, state, move):
        for rule in self.children:
            if not rule.legal(state, move):
                return False
        return True

    def list_legal(self, state):
        rule, *rules = self.children
        if rule.list_legal(state) == NotImplemented:
            return NotImplemented
        legal = rule.list_legal(state)
        for rule in rules:
            if rule.list_legal(state) == NotImplemented:
                return NotImplemented
            for move in legal:
                if move not in rule.list_legal(state):
                    legal.remove(move)
                    print(move)
                    print(state)
                    print(legal)
        return legal


class CrossProduct(Rule):
    def __init__(self, rule, *rules):
        self.children = rule, *rules

    def __repr__(self):
        return "(" + " * ".join([child.__repr__() for child in self.children]) + ")"

    def legal(self, state, move):
        move, *moves = move
        rule, *rules = self.children
        while moves and rules:
            if not rule.legal(state, move):
                return False
        if moves or rules:
            return False
        return True

    def list_legal(self, state):
        rule, *rules = self.children
        if rule.list_legal(state) is NotImplemented:
            return NotImplemented
        legal = rule.list_legal(state)
        for rule in rules:
            new_legal = []
            if rule.list_legal(state) is NotImplemented:
                return NotImplemented
            for move in legal:
                for comp in rule.list_legal(state):
                    new_legal.append((*move, comp))
            legal = new_legal
        return legal


class DotProduct(Rule):
    def __init__(self, rule, *rules):
        self.children = rule, *rules

    def __repr__(self):
        return "(" + " % ".join([child.__repr__() for child in self.children]) + ")"

    def legal(self, state, move):
        *move, moves = move
        *rules, rule = self.children
        while moves and rules:
            if not rule.legal(state, move):
                return False
            state = move(state)
        if moves or rules:
            return False
        return True

    def list_legal(self, state):
        *rules, rule = self.children
        if rule.list_legal(state) == NotImplemented:
            return NotImplemented
        legal = [Composition(move) for move in rule.list_legal(state)]
        for rule in rules:
            new_legal = []
            print(legal)
            if rule.list_legal(state) == NotImplemented:
                return NotImplemented
            for move in legal:
                for comp in rule.list_legal(state):
                    new_legal.append((*move, comp))
            legal = new_legal
        return legal


class ConstantRule(Rule):
    def __init__(self, moves):
        self.moves = moves

    def __repr__(self):
        return self.moves.__repr__()

    def legal(self, state, move):
        return move == self.moves

    def list_legal(self, state):
        return self.moves


if __name__ == "__main__":
    r = (ConstantRule([SumMove(1)]) | ConstantRule([SumMove(2)]) | PassRule()) & PassRule()
    p = PassRule()
    s = r % p % r
    print(r.list_legal(1))
    print(r)
    print(SumMove(2) == Identity())
    #print(s.list_legal( ((1,1), 1) ) )
