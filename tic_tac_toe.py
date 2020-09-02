from turn import SimpleTurn
from bit_rule import Unoccupied, RowPattern, ColumnPattern, DiagonalPattern


def tic_tac_toe(players=('x', 'o'), rows=3, columns=3, to_win=3):
    u = Unoccupied()
    r = RowPattern(rows, columns, to_win, *players)
    c = ColumnPattern(rows, columns, to_win, *players)
    d = DiagonalPattern(rows, columns, to_win, *players)
    t = SimpleTurn()
    g = t * (u - (r | c | d))
    s = g.create_state(seq=players, to_move=players[0],
                       **dict([(player, 0) for player in players]), total=rows * columns)
    return g, s


def tic_tac_toe_read(state, columns=3):
    state_string = state['to_move'] + '*'
    for x in range(state['total']):
        for player in state['seq']:
            if state[player] & (1 << x):
                state_string += player
                break
        else:
            state_string += '-'
        if not (x + 1) % columns:
            state_string += '\n  '
    return state_string


if __name__ == "__main__":
    game, game_state = tic_tac_toe()
    print(game)
    print(game.get_legal_moves(game_state))
    while game.get_legal_moves(game_state):
        print(tic_tac_toe_read(game.execute_move(game_state, game.get_legal_moves(game_state)[0]), 11))
        print(game.get_legal_moves(game_state))

