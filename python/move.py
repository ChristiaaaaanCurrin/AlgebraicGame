from abc import ABC, abstractmethod


class Move(ABC):
    @abstractmethod
    def __call__(self, state):
        pass

    @abstractmethod
    def get_inverse(self):
        pass

    def __mul__(self, other):
        return CartesianProduct(self, other)

    def __mod__(self, other):
        return Composition(self, other)


class Identity(Move):
    def __call__(self, state):
        return state

    def __eq__(self, other):
        return other == other.get_inverse()

    def __str__(self):
        return 'e'

    def get_inverse(self):
        return self


class CartesianProduct(Move):
    def __init__(self, *moves):
        self.children = moves

    def __call__(self, state):
        pass

    def __eq__(self, other):
        return type(self) == type(other) and self.children == other.children

    def __iter__(self):
        return self.children.__iter__()

    def __next__(self):
        return self.children.__next__()

    def get_inverse(self):
        return CartesianProduct(*[move.get_inverse() for move in self.children])


class Composition(Move):
    def __init__(self, *moves):
        self.children = moves

    def __call__(self, state):
        moves = self.children
        while moves:
            *moves, move = moves
            state = move(state)
        return state

    def __eq__(self, other):
        return type(self) == type(other) and self.children == other.children

    def __iter__(self):
        return self.children.__iter__()

    def __next__(self):
        return self.children.__next__()

    def get_inverse(self):
        return Composition(*[move.get_inverse() for move in self.children])


class SumMove(Move):
    def __init__(self, value):
        self.value = value

    def __call__(self, state):
        return state + self.value

    def get_inverse(self):
        return -self.value


if __name__ == '__main__':
    e = Identity()
    s = SumMove(1)
    m = s * s
    print(m(1))
    print(type([1, 'a', None]))
