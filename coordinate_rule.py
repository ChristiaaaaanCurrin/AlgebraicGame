from rule import Rule
from abc import ABC


class CoordinateRule(Rule, ABC):
    def __init__(self, *keys, **kwargs):
        self.keys = keys
        super().__init__(**kwargs)

    def state_requirements(self):
        req = {}
        for key in self.keys:
            req[key] = []
        return req

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
        old_coords, new_coords = move
        if self.remove_coords(state, old_coords, *self.keys) and self.add_coords(state, new_coords, *self.keys):
            return state
        else:
            return False

    def undo_move(self, state, move):
        old_coords, new_coords = move
        if self.remove_coords(state, new_coords, *self.keys) and self.add_coords(state, old_coords, *self.keys):
            return state
        else:
            return False

