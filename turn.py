from rule import Rule


class SimpleTurn(Rule):
    def __repr__(self):
        return 'SimpleTurn'

    def state_requirements(self):
        return {'turn': 0, 'seq': ['p1'], 'to_move': 'p1'}

    def get_legal_moves(self, state):
        return [1]

    def does_decorate(self, *move, state):
        return True

    def execute_move(self, move, state):
        state['turn'] = (state['turn'] + move) % len(state['seq'])
        state['to_move'] = state['seq'][state['turn']]
        return state

    def undo_move(self, move, state):
        state['turn'] = (state['turn'] + move) % len(state['seq'])
        state['to_move'] = state['seq'][state['turn']]
        return state


if __name__ == "__main__":
    game = SimpleTurn()
    game_state = game.create_state(seq=['x', 'o'])
    print(game_state.game.get_legal_moves(game_state))

