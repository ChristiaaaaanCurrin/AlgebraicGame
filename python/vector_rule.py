from python.rule import Rule


class FindPiece (Rule):
    def __init__(self, keys):
        self.keys = keys
    def state_requirements(self):
        pass

    def get_legal_moves(self, state):
        pass

    def execute_move(self, state, move):
        pass

    def undo_move(self, state, move):
        pass


class