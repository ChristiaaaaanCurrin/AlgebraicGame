from abc import ABC, abstractmethod


class Move(ABC):
    @abstractmethod
    def __call__(self, state):
        pass

    @abstractmethod
    def get_inverse(self):
        pass

    def __mul__(self, other):
        return ParallelMove(self, other)

    def __mod__(self, other):
        return Composition(self, other)


class Identity(Move):
    def __call__(self, state):
        return state

    def __eq__(self, other):
        return type(self) == type(other) or other == other.get_inverse()

    def __repr__(self):
        return "e"

    def get_inverse(self):
        return self


class ParallelMove(Move):
    def __init__(self, *moves):
        self.children = moves

    def __call__(self, state):
        moves = self.children
        states = state
        new_state = ()
        while moves and states:
            move, *moves = moves
            state, *states = states
            new_state = *new_state, move(state)
        assert not moves, "The Move is Bigger than the State"
        assert not states, "The State is Bigger than the Move"
        return new_state

    def __eq__(self, other):
        return type(self) == type(other) and self.children == other.children

    def __repr__(self):
        return "(" + ", ".join([child.__repr__() for child in self.children]) + ")"

    def __iter__(self):
        return self.children.__iter__()

    def __next__(self):
        return self.children.__next__()

    def get_inverse(self):
        return ParallelMove(*[move.get_inverse() for move in self.children])


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

    def __repr__(self):
        return " o ".join([child.__repr__() for child in self.children])

    def __iter__(self):
        return self.children.__iter__()

    def __next__(self):
        return self.children.__next__()

    def get_inverse(self):
        return Composition(*[move.get_inverse() for move in self.children])


class SumMove(Move):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "s" + self.value.__repr__()

    def __call__(self, state):
        return state + self.value

    def get_inverse(self):
        return SumMove(-self.value)


if __name__ == '__main__':
    e = Identity()
    s = SumMove(1)
    m = s.get_inverse() % e % s % s
    print(m(1))
