from rule import Rule


class UnoccupiedCoord(Rule):
    def __init__(self, total, only_on_turn=True, **kwargs):
        self.on_turn = only_on_turn
        self.total = total
        super().__init__(**kwargs)

    def __repr__(self):
        return 'UnoccupiedCoord' + str(self.total)

    def state_requirements(self):
        return {'players': {}, 'to_move': None}

    def get_legal_moves(self, state):
        legal = []
        agents = [state['to_move']] if self.on_turn else state['players']
        for agent in agents:
            for n in range(self.total):
                for player, occupancy in state['players'].items():
                    if (1 << n) & occupancy:
                        break
                else:
                    legal.append((agent, n))
        return legal

    def execute_move(self, move, state):
        player, move = move
        state['players'][player] = state['players'][player] | (1 << move)
        return state

    def undo_move(self, move, state):
        player, move = move
        state['players'][player] = state['players'][player] & (~ move)
        return state


