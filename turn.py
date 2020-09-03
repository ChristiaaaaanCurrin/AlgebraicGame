from rule import Rule, ZeroRule, Countable


class SimpleTurn(Countable):
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


class NotOnTurn(ZeroRule):
    def state_requirements(self):
        return {'to_move': ''}

    def legal(self, state, move):
        for sub_move in move:
            if state['to_move'] in sub_move:
                return False
        else:
            return True
