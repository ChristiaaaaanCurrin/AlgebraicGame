from turn import SimpleTurn
from bit_rule import Unoccupied, RowPattern, ColumnPattern, DiagonalPattern


def tic_tac_toe(players=('x', 'o'), rows=3, columns=3, to_win=3):
    u = Unoccupied()
    r = RowPattern(rows, columns, to_win, *players)
    c = ColumnPattern(rows, columns, to_win, *players)
    d = DiagonalPattern(rows, columns, to_win, *players)
    t = SimpleTurn()
    g = t * (u - (r + c + d))
    s = g.create_state(seq=players,
                       to_move=players[0],
                       **dict([(player, 0) for player in players]),
                       total=rows * columns)
    return g, s


if __name__ == "__main__":
    game, state = tic_tac_toe()
    print(game)
    print(game.get_legal_moves(state))
    print(game.execute_move(state, game.get_legal_moves(state)[0]))
    print(game.get_legal_moves(state))

