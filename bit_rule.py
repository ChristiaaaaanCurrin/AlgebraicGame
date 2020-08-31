from rule import Rule, ZeroRule


class Unoccupied(Rule):
    def __init__(self, *keys, **kwargs):
        self.keys = keys
        super().__init__(**kwargs)

    def __repr__(self):
        return f'Unoccupied: {self.keys}'

    def state_requirements(self):
        if self.keys:
            return {'total': 0, **dict([(key, 0) for key in self.keys])}
        else:
            return {'total': 0, 'to_move': '', 'seq': ['']}

    def get_legal_moves(self, state):
        legal = []
        check_keys = self.keys if self.keys else [state['to_move']]
        against_keys = check_keys if self.keys else state['seq']
        for check_key in check_keys:
            for n in range(state['total']):
                for against_key in against_keys:
                    if (1 << n) & state[against_key]:
                        break
                else:
                    legal.append((check_key, n))
        return legal

    def execute_move(self, state, move):
        key, move = move
        state[key] = state[key] | (1 << move)
        return state

    def undo_move(self, state, move):
        key, move = move
        state[key] = state[key] & (~ move)
        return state


class RowPattern(ZeroRule):
    def __init__(self, rows, columns, pattern_length, *keys, **kwargs):
        self.rows = rows
        self.columns = columns
        self.pattern_length = pattern_length
        self.keys = keys

        self.detection_masks = []
        row_mask = (1 << pattern_length) - 1
        for r in range(rows):
            self.detection_masks.append(row_mask)
            for c in range(columns - pattern_length):
                row_mask = row_mask << 1
                self.detection_masks.append(row_mask)
            row_mask = row_mask << pattern_length

        super().__init__(**kwargs)

    def __repr__(self):
        return f'RowPattern: {self.rows}x{self.columns}, {self.pattern_length}, {self.keys}'

    def state_requirements(self):
        return dict([(key, 0) for key in self.keys])

    def legal(self, state, move):
        for key in self.keys:
            for mask in self.detection_masks:
                if not ((~state[key]) & mask):
                    return True
        else:
            return False


class ColumnPattern(ZeroRule):
    def __init__(self, rows, columns, pattern_length, *keys, **kwargs):
        self.rows = rows
        self.columns = columns
        self.pattern_length = pattern_length
        self.keys = keys

        self.detection_masks = []
        column_mask = 1
        for w in range(pattern_length - 1):
            column_mask = 1 | (column_mask << columns)
        for c in range(columns):
            self.detection_masks.append(column_mask)
            for r in range(rows - pattern_length):
                column_mask = column_mask << columns
                pattern_length.append(column_mask)
            column_mask = column_mask << 1

        super().__init__(**kwargs)

    def __repr__(self):
        return f'ColumnPattern: {self.rows}x{self.columns}, {self.pattern_length}, {self.keys}'

    def state_requirements(self):
        return dict([(key, 0) for key in self.keys])

    def legal(self, state, move):
        for key in self.keys:
            for mask in self.detection_masks:
                if not ((~state[key]) & mask):
                    return True
        else:
            return False


class DiagonalPattern(ZeroRule):
    def __init__(self, rows, columns, pattern_length, *keys, **kwargs):
        self.rows = rows
        self.columns = columns
        self.pattern_length = pattern_length
        self.keys = keys

        self.detection_masks = []
        diagonal_mask = 1
        for w in range(pattern_length - 1):
            diagonal_mask = diagonal_mask | (diagonal_mask << (columns + 1))
        for r in range(rows - pattern_length + 1):
            for c in range(columns - pattern_length + 1):
                self.detection_masks.append(diagonal_mask)
                diagonal_mask = diagonal_mask << 1
            diagonal_mask = diagonal_mask << pattern_length

        diagonal_mask = 1 << (columns - 1)
        for w in range(pattern_length - 1):
            diagonal_mask = diagonal_mask | (diagonal_mask << (columns - 1))
        for r in range(rows - pattern_length + 1):
            for c in range(columns - pattern_length + 1):
                self.detection_masks.append(diagonal_mask)
                diagonal_mask = diagonal_mask >> 1
            diagonal_mask = diagonal_mask << pattern_length

        super().__init__(**kwargs)

    def __repr__(self):
        return f'DiagonalPattern: {self.rows}x{self.columns}, {self.pattern_length}, {self.keys}'

    def state_requirements(self):
        return dict([(key, 0) for key in self.keys])

    def legal(self, state, move):
        for key in self.keys:
            for mask in self.detection_masks:
                if not ((~state[key]) & mask):
                    return True
        else:
            return False
