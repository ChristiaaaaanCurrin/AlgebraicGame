from rule import Rule
from turn import SimpleTurn
from coordinate_rule import CoordinateRule


class Check(Rule):
    def __repr__(self):
        return 'Check'

    def state_requirements(self):
        return {'king': [], 'to_move': 'w', 'seq': ['w', 'b'], 'w': [], 'b': []}

    def execute_move(self, state, move):
        return False

    def undo_move(self, state, move):
        return False

    def get_legal_moves(self, state):
        return []

    def legal(self, state, move):
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


if __name__ == "__main__":
    game = SimpleTurn() * Check()
    game_state = game.create_state(king=(0,), y=(0,))
    print(game)
    print(game_state)
    print(list(game.get_legal_moves(game_state)))