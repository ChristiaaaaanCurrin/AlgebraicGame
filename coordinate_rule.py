from rule import Rule, ZeroRule
from abc import ABC


class CoordinateMoveRule(Rule, ABC):
    def __init__(self, *keys, on_turn=True, **kwargs):
        self.keys = keys
        self.on_turn = on_turn
        super().__init__(**kwargs)

    def state_requirements(self):
        key_requirements = dict([(key, []) for key in self.keys])
        return {'to_move': '', **key_requirements} if self.on_turn else key_requirements

    @staticmethod
    def add_coords(state, coords, *keys):
        for key in keys:
            state[key].append(coords)
        return state

    @staticmethod
    def remove_coords(state, coords, *keys):
        if coords in state.key_intersection(*keys):
            for key in keys:
                state[key].remove(coords)
            return state
        else:
            return False

    def execute_move(self, state, move):
        old_coords, new_coords, *keys = move
        if self.remove_coords(state, old_coords, *keys) and self.add_coords(state, new_coords, *keys):
            return state
        else:
            return False

    def undo_move(self, state, move):
        old_coords, new_coords, *keys = move
        if self.remove_coords(state, new_coords, *keys) and self.add_coords(state, old_coords, *keys):
            return state
        else:
            return False


class OutOfBoard(ZeroRule):
    def state_requirements(self):
        return {'board': []}

    def legal(self, state, move):
        old_coords, new_coords, *keys = move
        for index, component in enumerate(new_coords):
            if not 0 <= component < state['board'][index]:
                return True
        else:
            return False


class SimpleCartesianMove(CoordinateMoveRule):
    def __init__(self, steps, coord_indices, *keys, **kwargs):
        self.steps = steps
        self.coord_indices = coord_indices
        super().__init__(*keys, **kwargs)

    def get_legal_moves(self, state):
        legal = []
        keys = [*self.keys]
        if self.on_turn:
            keys.append(state['to_move'])
        for old_coords in state.key_intersection(*keys):
            for step in self.steps:
                for index in self.coord_indices:
                    new_coords = list(old_coords)
                    new_coords[index] = new_coords[index] + step
                    legal.append((old_coords, tuple(new_coords), *keys))
        return legal

