from rule import Rule
from turn import SimpleTurn


class Check(Rule):
    def __repr__(self):
        return 'Check'

    def state_requirements(self):
        return {'king': [], 'to_move': 'w', 'seq': ['w', 'b'], 'w': [], 'b': []}

    def execute_move(self, move, state):
        return False

    def undo_move(self, move, state):
        return False

    def get_legal_moves(self, state):
        return []

    def legal(self, move, state):
        player = state['to_move']
        state = state.game.execute_move(move, state)
        legal = self.in_check(player, state)
        state.game.undo_move(move, state)
        return legal

    @staticmethod
    def in_check(player, state):
        for king in state.key_intersection('king', player):
            if king in state.game.get_legal_moves(state):
                return True
        else:
            return False


class King(Rule):

    def state_requirements(self):
        return {'K': []}

    def get_legal_moves(self, state):
        for coords in state.key_intersection('K', state['to_move']):
            pass

    def execute_move(self, move, state):
        pass

    def undo_move(self, move, state):
        pass


if __name__ == "__main__":
    game = SimpleTurn() * Check()
    game_state = game.create_state(king=(0,), y=(0,))
    print(game)
    print(game_state)
    print(list(game.get_legal_moves(game_state)))