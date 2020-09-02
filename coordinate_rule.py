from rule import Rule, ZeroRule
from abc import ABC


class CoordinatePiece:
    def __init__(self, coords, *keys):
        self.coords = coords
        self.keys = keys

    def __eq__(self, other):
        return self.coords == other.coords and self.keys == other.keys

    def __repr__(self):
        return f'{"".join(self.keys), self.coords}'

    def __add__(self, other):
        new_coords = tuple([old_coord + other.coords[i] for i, old_coord in enumerate(self.coords)])
        return CoordinatePiece(new_coords, *self.keys, *other.keys)

    def __sub__(self, other):
        new_coords = tuple([old_coord - other.coords[i] for i, old_coord in enumerate(self.coords)])
        return CoordinatePiece(new_coords, *filter(lambda x: x not in other.keys, self.keys))

    def __neg__(self):
        new_coords = tuple([-coord for coord in self.coords])
        return CoordinatePiece(new_coords, *self.keys)

    def add_to_state(self, state):
        for key in self.keys:
            state[key].append(self)

    def remove_from_state(self, state):
        for key in self.keys:
            if self in state[key]:
                state[key].remove(self)


class CoordinateRule(Rule, ABC):
    def __init__(self, *keys, on_turn=True, **kwargs):
        self.keys = keys
        self.on_turn = on_turn
        super().__init__(**kwargs)

    def state_requirements(self):
        key_requirements = dict([(key, []) for key in self.keys])
        return {'to_move': '', **key_requirements} if self.on_turn else key_requirements


class OutOfBoard(ZeroRule):
    def __repr__(self):
        return 'OutOfBoard'

    def state_requirements(self):
        return {'board': []}

    def legal(self, state, move):
        piece, delta = move
        for index, component in enumerate((piece + CoordinatePiece(delta)).coords):
            if not 0 <= component < state['board'][index]:
                return True
        else:
            return False


class CoordinateMoveRule(CoordinateRule, ABC):
    def execute_move(self, state, move):
        piece, delta = move
        piece += CoordinatePiece(delta)
        return state

    def undo_move(self, state, move):
        piece, delta = move
        piece -= CoordinatePiece(delta)
        return state


class SimpleCartesianMove(CoordinateMoveRule):
    def __init__(self, steps, coord_indices, *keys, **kwargs):
        self.steps = steps
        self.coord_indices = coord_indices
        super().__init__(*keys, **kwargs)

    def __repr__(self):
        return 'CartesianMove'

    def get_legal_moves(self, state):
        legal = []
        keys = [*self.keys]
        if self.on_turn:
            keys.append(state['to_move'])
        for piece in state.key_intersection(*keys):
            for step in self.steps:
                new_coords = [0] * len(piece.coords)
                for i in self.coord_indices:
                    new_coords[i] = [i]
                    legal.append((piece, tuple(new_coords)))
        return legal


class CaptureRule(CoordinateRule, ABC):
    def get_legal_moves(self, state):
        return state.key_intersection(self.keys)

    def execute_move(self, state, move):
        for piece in move:
            piece.remove_from_state(state)
        return state

    def undo_move(self, state, move):
        for piece in move:
            piece.add_to_state(state)
        return state


class SimpleCapture(CaptureRule):
    def does_decorate(self, state, move):
        piece, *move = move
        if piece.coords in move:
            return True
        else:
            return False
