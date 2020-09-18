from python.rule import Rule


class SimpleTurn(Rule):
    def __repr__(self):
        return 'SimpleTurn'

    def state_requirements(self):
        return {'turn': 0, 'seq': ['p1'], 'to_move': 'p1'}

    def get_legal_moves(self, state):
        return [1]

    def execute_move(self, state, move):
        state['turn'] = (state['turn'] + move) % len(state['seq'])
        state['to_move'] = state['seq'][state['turn']]
        return state

    def undo_move(self, state, move):
        state['turn'] = (state['turn'] + move) % len(state['seq'])
        state['to_move'] = state['seq'][state['turn']]
        return state
