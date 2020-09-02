from rule import Rule
from turn import SimpleTurn
from coordinate_rule import SimpleCartesianMove, OutOfBoard, CoordinatePiece


class Check(Rule):
    def __init__(self, game, **kwargs):
        self.game = game
        super().__init__(**kwargs)

    def __repr__(self):
        return 'Check'

    def state_requirements(self):
        return {'king': [], 'to_move': 'w'}

    def execute_move(self, state, move):
        return False

    def undo_move(self, state, move):
        return False

    def get_legal_moves(self, state):
        return []

    def legal(self, state, move):
        player = state['to_move']
        state = self.game.execute_move(move, state)
        legal = self.in_check(player, state)
        state.game.undo_move(move, state)
        return legal

    def in_check(self, player, state):
        for king in state.key_intersection('king', player):
            if king in self.game.get_legal_moves(state):
                return True
        else:
            return False


def traditional_chess(players=('w', 'b'), ranks=8, files=8, *pieces):
    pass


if __name__ == "__main__":
    border = OutOfBoard()
    square = SimpleCartesianMove((1, -1), (0, 1), 'K')
    diagonal = square * square
    king = diagonal - border

    game = SimpleTurn() * king
    test_king = CoordinatePiece((0, 1), 'K', 'y', 'king')
    game_state = game.create_state(to_move='y', seq=['y', 'b'], board=[4, 4], y=[], b=[], king=[])
    test_king.add_to_state(game_state)

    print(game)
    print(game_state)
    print(game.get_legal_moves(game_state))
