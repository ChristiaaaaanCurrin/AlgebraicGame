from python.rule import Rule, RulePattern, TrueRule, ZeroRule
from python.turn import SimpleTurn
from python.vector_rule import SimpleCapture, VectorPiece, VectorMoveRule, EuclideanBoard, VectorMoveExtension


class Check(Rule):
    def __init__(self, game, **kwargs):
        self.game = game
        super().__init__(**kwargs)

    def __repr__(self):
        return 'Check'

    def state_requirements(self):
        return {'to_move': 'w', **dict([(key, []) for key in self.keys])}

    def execute_move(self, state, move):
        return False

    def undo_move(self, state, move):
        return False

    def legal(self, state, move):
        player = state['to_move']
        state = self.game.execute_move(state, move)
        legal = [move] if self.in_check(player, state) else []
        self.game.undo_move(state, move)
        return legal

    def in_check(self, player, state):
        for king in state.key_intersection(*self.keys, player):
            for to_capture, move in self.game.get_legal_moves(state):
                if king in to_capture:
                    return True
        else:
            return False


def traditional_chess(players=('w', 'b'), ranks=8, files=8, *pieces):
    piece_keys = [*'KQNBRP']
    board = EuclideanBoard(files, ranks)
    king = (VectorMoveRule((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1),
                           (1, 0), (1, 1), keys='K') - board) ** SimpleCapture(keys=piece_keys)

    bishop = (RulePattern(VectorMoveExtension((-1, -1), (1, 1), (-1, 1), (1, -1)),
                          VectorMoveRule((0, 0), keys='B'),
                          TrueRule(),
                          ZeroRule()) - board) ** SimpleCapture(keys=piece_keys)

    game = SimpleTurn() * ((king + bishop) - Check(king, keys='k'))

    game_state = game.create_state(to_move=players[0], seq=players, w=[], b=[], k=[])

    for piece in pieces:
        keys, *coords = piece.split('.')
        coords = [int(coord) for coord in coords]
        VectorPiece(coords=coords, keys=keys).add_to_state(game_state)

    return game, game_state


if __name__ == "__main__":
    test_game, test_game_state = traditional_chess(('w', 'b'), 8, 8, 'Kb.0.0', 'Bw.0.1')
    print(test_game)
    print(test_game_state)
    print(test_game.get_legal_moves(test_game_state))
    print(test_game.execute_move(test_game_state, test_game.get_legal_moves(test_game_state)[0]))
