from abc import ABC, abstractmethod
from random import sample, random


class Evaluator(ABC):
    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)
        super().__init__()

    @abstractmethod
    def evaluate(self, state):
        """
        :param state: game state to be evaluated
        :return: evaluation of game, (dictionary of values keyed by players)
        """
        pass

    def explore(self, game, state, depth, width=-1, temp=1, k=1):
        """
        searches game tree and applies max_n algorithm to evaluate current game
        :param state: game state to be explored
        :param game: game to guide search tree
        :param depth: maximum depth of search
        :param width: maximum branches from this node
        :param temp: probability of selecting the child branches randomly
        :param k: depth of intermediate searches for determining continuation line
        :return: evaluation of current game ( = utility from the end of the expected branch)
        """
        player = state['to_move']
        legal = game.get_legal_moves(state)
        if 0 <= width < len(legal):
            if temp < random():
                def evaluate(m):
                    game.execute_move(state, m)
                    utility = self.explore(game, state, k)[player]
                    game.undo_move(state, m)
                    return utility
                legal = sorted(legal, key=evaluate)[:width]
            else:
                legal = sample(game.get_legal_moves(), width)
        if depth == 0 or not legal:
            return self.evaluate(state)
        else:
            utilities = []
            for move in legal:
                game.execute_move(state, move)
                utilities.append(self.explore(game, state, depth - 1, width, temp))
                game.undo_move(state, move)
            return max_by_key(player, utilities)


class ZeroSum(Evaluator):
    def __init__(self, *evaluators, **kwargs):
        self.evaluators = evaluators
        super().__init__(**kwargs)

    def evaluate(self, state):
        utilities = {}
        for evaluator in self.evaluators:
            utilities.update(evaluator.evaluate(state))
        total = 0
        for player, utility in utilities.items():
            total += utility
        for player in utilities:
            utilities[player] = utilities[player] / total if total else 1 / len(utilities)
        return utilities


class WinLose(Evaluator):
    def __init__(self, *wins, **kwargs):
        self.wins = wins
        super().__init__(**kwargs)

    def evaluate(self, state):
        utility = {}
        for player, win in self.wins:
            if win.get_legal_moves(state):
                utility[player] = 1
            else:
                utility[player] = 0
        return utility


def max_by_key(key, dictionaries):
    """
    :param key: a key in the dictionary
    :param dictionaries: list of dictionaries with the same keys, dictionary entries must be ordered (<, > defined)
    :return: the dictionary where the value of dictionary[key] is maximized
    """
    current_max = dictionaries[0]
    for dictionary in dictionaries:
        if dictionary[key] > current_max[key]:
            current_max = dictionary
    return current_max


if __name__ == "__main__":
    pass
