from abc import ABC, abstractmethod
from move import Identity


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
        return self * Pass() | Pass() * other


class Void(Rule):
    def legal(self, state, move):
        return False

    def list_legal(self, state):
        return []

    def __or__(self, other):
        return other

    def __and__(self, other):
        return self

    def __mul__(self, other):
        return self


class Pass(Rule):
    def legal(self, state, move):
        return move.get_inverse() == move

    def list_legal(self, state):
        return Identity()


class Union(Rule):
    def __init__(self, rule, *rules):
        self.children = (rule, *rules)

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
                if move not in rule.list_legal():
                    legal.remove(move)
        return legal


class CrossProduct(Rule):
    def __init__(self, rule, *rules):
        self.children = rule, *rules

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
        if rule.list_legal(state) == NotImplemented:
            return NotImplemented
        legal = rule.list_legal(state)
        for rule in rules:
            new_legal = []
            if rule.list_legal(state) == NotImplemented:
                return NotImplemented
            for move in legal:
                for comp in rule.list_legal(state):
                    new_legal.append((*move, comp))
            legal = new_legal
        return legal


class DotProduct(Rule):
    def __init__(self, rule, *rules):
        self.children = rule, *rules

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
        legal = rule.list_legal(state)
        for rule in rules:
            new_legal = []
            if rule.list_legal(state) == NotImplemented:
                return NotImplemented
            for move in legal:
                for comp in rule.list_legal(state):
                    new_legal.append((*move, comp))
            legal = new_legal
        return legal


class ConstantRule(Rule):
    def __init__(self, move):
        self.move = move

    def legal(self, state, move):
        return move == self.move

    def list_legal(self, state):
        return self.move


print(2 ^ 3)
