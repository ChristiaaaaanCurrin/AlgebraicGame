from rule import Rule


class BitOccupancy(Rule):
    def __init__(self, only_on_turn=True, **kwargs):
        self.on_turn = only_on_turn
        super().__init__(**kwargs)

    def __repr__(self):
        return 'BitOccupancy'

    def state_requirements(self):
        return {'players': {}, 'to_move': None, 'total': 0} if self.on_turn else {'players': {}, 'total': 0}

    def get_legal_moves(self, state):
        legal = []
        agents = [state['to_move']] if self.on_turn else state['players']
        for agent in agents:
            for n in range(state['total']):
                for player, occupancy in state['players'].items():
                    if (1 << n) & occupancy:
                        break
                else:
                    legal.append((agent, n))
        return legal

    def execute_move(self, state, move):
        player, move = move
        state['players'][player] = state['players'][player] | (1 << move)
        return state

    def undo_move(self, state, move):
        player, move = move
        state['players'][player] = state['players'][player] & (~ move)
        return state


