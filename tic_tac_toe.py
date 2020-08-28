from rule import Rule
from turn import SimpleTurn
from coordinate_rule import UnoccupiedCoord


class TicTacToeWin(Rule):
    def __init__(self, **kwargs):
        kwargs = {'to_win': 3, 'rows': 3, 'columns': 3, **kwargs}
        self.rows = kwargs.pop('rows')
        self.columns = kwargs.pop('columns')
        self.to_win = kwargs.pop('to_win')
        self.win_masks = self.generate_win_masks(self.to_win, self.rows, self.columns)
        super().__init__(**kwargs)

    def __repr__(self):
        return 'TicTacToeWin: ' + str(self.to_win)

    def generate_win_masks(self, to_win, rows, columns):
        return [*self.generate_row_masks(to_win, rows, columns),
                *self.generate_column_masks(to_win, rows, columns),
                *self.generate_diagonal_masks(to_win, rows, columns)]

    @staticmethod
    def generate_row_masks(to_win, rows, columns):
        win_masks = []
        row_mask = (1 << to_win) - 1
        for r in range(rows):
            win_masks.append(row_mask)
            for c in range(columns - to_win):
                row_mask = row_mask << 1
                win_masks.append(row_mask)
            row_mask = row_mask << to_win
        return win_masks

    @staticmethod
    def generate_column_masks(to_win, rows, columns):
        win_masks = []
        column_mask = 1
        for w in range(to_win - 1):
            column_mask = 1 | (column_mask << columns)
        for c in range(columns):
            win_masks.append(column_mask)
            for r in range(rows - to_win):
                column_mask = column_mask << columns
                win_masks.append(column_mask)
            column_mask = column_mask << 1
        return win_masks

    @staticmethod
    def generate_diagonal_masks(to_win, rows, columns):
        win_masks = []
        diagonal_mask = 1
        for w in range(to_win - 1):
            diagonal_mask = diagonal_mask | (diagonal_mask << (columns + 1))
        for r in range(rows - to_win + 1):
            for c in range(columns - to_win + 1):
                win_masks.append(diagonal_mask)
                diagonal_mask = diagonal_mask << 1
            diagonal_mask = diagonal_mask << to_win

        diagonal_mask = 1 << (columns - 1)
        for w in range(to_win - 1):
            diagonal_mask = diagonal_mask | (diagonal_mask << (columns - 1))
        for r in range(rows - to_win + 1):
            for c in range(columns - to_win + 1):
                win_masks.append(diagonal_mask)
                diagonal_mask = diagonal_mask >> 1
            diagonal_mask = diagonal_mask << to_win
        return win_masks

    def state_requirements(self):
        return {"players": {'x': 0, 'o': 0}}

    def legal(self, move, state):
        for player, occupancy in state['players'].items():
            for mask in self.win_masks:
                if not ((~occupancy) & mask):
                    return True
        else:
            return False

    def get_legal_moves(self, state):
        return []

    def execute_move(self, move, state):
        return False

    def undo_move(self, move, state):
        return False


if __name__ == "__main__":
    u = UnoccupiedCoords(9)
    w = TicTacToeWin()
    t = SimpleTurn()
    g = t * (u - w)
    s = g.create_state(seq=['x', 'o'], to_move='x')
    print(s)
    print(g.get_legal_moves(s))
    print(g.execute_move(g.get_legal_moves(s)[8], s))
    print(u.execute_move(['x', 1], s))
    print((u - w).execute_move(['x', 2], s))
