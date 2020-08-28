from rule import Rule


class Check(Rule):
    def __repr__(self):
        return 'Check'

    def state_requirements(self):
        return {'king': [], 'to_move': 'w', 'seq': ['w', 'b'], 'w': [], 'b': []}

    def execute_move(self, move, state):
        return False

    def undo_move(self, move, state):
        return False

    def get_legal_moves(self, state):
        return []

    def legal(self, move, state):
        player = state['to_move']
        state = state.game.execute_move(move, state)
        legal = self.in_check(player, state)
        state.game.undo_move(move, state)
        return legal

    @staticmethod
    def in_check(player, state):
        for king in state.key_intersection('king', player):
            for rule in state.game.flatten():
                if king in rule.get_legal_moves(state):
                    return True
        else:
            return False


if __name__ == "__main__":
    game = Check()
    game_state = game.create_state()
    print(game)
    print(game_state)