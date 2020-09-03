from turn import SimpleTurn
from bit_rule import Unoccupied, RowPattern, ColumnPattern, DiagonalPattern
from rule import ZeroRule
from evaluator import ZeroSum, WinLose


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


def tic_tac_toe_evaluator(players=('x', 'o'), rows=3, columns=3, to_win=3):
    wins = []
    for player in players:
        r = RowPattern(rows, columns, to_win, player)
        c = ColumnPattern(rows, columns, to_win, player)
        d = DiagonalPattern(rows, columns, to_win, player)
        wins.append((player, d | c | r))
    return ZeroSum(WinLose(*wins))


if __name__ == "__main__":
    game, game_state = tic_tac_toe()
    turn, other = game
    un, win = other
    rc, d = win
    r, c = rc
    [print(mask) for mask in d.detection_masks]
    print(game)
    evaluator = tic_tac_toe_evaluator()
    for n in range(1):
        print(game.get_legal_moves(game_state))
        print(r.legal(game_state, ''))
        print(c.legal(game_state, ''))
        print(d.legal(game_state, ''))
        game.execute_move(game_state, game.get_legal_moves(game_state)[0])
    print(evaluator.explore(game, game_state, -1))

