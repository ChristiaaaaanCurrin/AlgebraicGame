from rule import Rule, ZeroRule


class SimpleTurn(Rule):
    def __repr__(self):
        return 'SimpleTurn'

    def state_requirements(self):
        return {'turn': 0, 'seq': ['p1'], 'to_move': 'p1'}

    def get_legal_moves(self, state):
        return [1]

    def does_decorate(self, state, move):
        return True

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


if __name__ == "__main__":
    game = SimpleTurn()
    game_state = game.create_state(seq=['x', 'o'])
    print(game_state.game.get_legal_moves(game_state))

