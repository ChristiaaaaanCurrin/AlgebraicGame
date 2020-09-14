from rule import Countable, Rule
from abc import ABC
from numpy import array, zeros_like


class VectorPiece:
    def __init__(self, coords, keys):
        self.coords = array(coords)
        self.keys = keys

    def __eq__(self, other):
        return (self.coords == other.coords).all and self.keys == other.keys

    def __repr__(self):
        return f'{"".join(self.keys), self.coords}'

    def __str__(self):
        return str(tuple(self.coords))

    def add_to_state(self, state):
        for key in self.keys:
            state[key].append(self)

    def remove_from_state(self, state):
        for key in self.keys:
            if self in state[key]:
                state[key].remove(self)


# -- Moving -----------------------------------------------

class VectorMoveRule(Countable):
    def __init__(self, *deltas, **kwargs):
        super().__init__(**kwargs)
        self.deltas = [array(delta) for delta in deltas]

    def __repr__(self):
        return str(self.keys) + str(list(map(tuple, self.deltas)))

    def __str__(self):
        return str(self.keys)

    def get_legal_moves(self, state):
        legal = []
        pieces = state.key_intersection(*self.keys)
        for piece in pieces:
            for delta in self.deltas:
                legal.append((piece, delta))
        return legal

    def execute_move(self, state, move):
        piece, delta = move
        piece.coords += delta
        return state

    def undo_move(self, state, move):
        piece, delta = move
        piece.coords -= delta
        return state

    def state_requirements(self):
        return dict([(key, []) for key in self.keys])


class VectorMoveExtension(Rule):
    def __init__(self, *deltas, **kwargs):
        super().__init__(**kwargs)
        self.deltas = [array(delta) for delta in deltas]

    def legal(self, state, move):
        piece, coords = move
        return [(piece, coords + delta) for delta in self.deltas]

    def state_requirements(self):
        return {}

    def execute_move(self, state, move):
        piece, delta = move
        piece.coords += delta
        return state

    def undo_move(self, state, move):
        piece, delta = move
        piece.coords -= delta
        return state


# -- Capturing --------------------------------------------

class WithCapture(Rule, ABC):
    def state_requirements(self):
        return dict([(key, []) for key in self.keys])

    def execute_move(self, state, move):
        for piece in move:
            piece.remove_from_state(state)
        return state

    def undo_move(self, state, consequence):
        for piece in consequence:
            piece.add_to_state(state)
        return state


class SimpleCapture(WithCapture):
    def __repr__(self):
        return 'SimpleCapture: ' + str(self.keys)

    def legal(self, state, move):
        to_capture = []
        attacker, delta = move
        pieces = state.key_union(*self.keys)
        for piece in pieces:
            if (piece.coords == attacker.coords + delta).all():
                to_capture.append(piece)
        return to_capture


class RemoteCapture(WithCapture):
    def __init__(self, *deltas, **kwargs):
        self.deltas = deltas
        super().__init__(**kwargs)

    def legal(self, state, move):
        to_capture = []
        attacker, move_delta = move
        pieces = state.key_intersection(*self.keys)
        for piece in pieces:
            for capture_delta in self.deltas:
                if (piece.coords + capture_delta == attacker.coords + move_delta).all():
                    to_capture.append(piece)
        return to_capture


# -- Board ------------------------------------------------

class EuclideanBoard(Rule):
    def __init__(self, *dimensions, **kwargs):
        self.dimensions = array(dimensions)
        self.zeros = zeros_like(self.dimensions)
        super().__init__(**kwargs)

    def __repr__(self):
        return 'EuclideanBoard: ' + str(self.dimensions)

    def legal(self, state, move):
        piece, delta = move
        if (self.zeros <= piece.coords + delta).all() and (piece.coords + delta < self.dimensions).all():
            return False
        else:
            return True

    def execute_move(self, state, move):
        return False

    def undo_move(self, state, move):
        return False

    def state_requirements(self):
        return {}
