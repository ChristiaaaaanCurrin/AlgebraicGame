from abc import ABC, abstractmethod
from random import sample, random


class Evaluator(ABC):
    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)
        super().__init__()

    @abstractmethod
    def evaluate(self, game):
        """
        :param game: game to be evaluated
        :return: evaluation of game, (dictionary of values keyed by players)
        """
        pass

    def explore(self, game, depth, width=-1, temp=1, k=1):
        """
        searches game tree and applies max_n algorithm to evaluate current game
        :param game: game to be explored
        :param depth: maximum depth of search
        :param width: maximum branches from this node
        :param temp: probability of selecting the child branches randomly
        :param k: depth of intermediate searches for determining continuation line
        :return: evaluation of current game ( = utility from the end of the expected branch)
        """
        player = game.get_player()
        legal = game.get_legal_moves()
        if 0 <= width < len(legal):
            if temp < random():
                def evaluate(m):
                    game.execute_move(m)
                    utility = self.explore(game, k)[player]
                    game.undo_move(m)
                    return utility
                legal = sorted(legal, key=evaluate)[:width]
            else:
                legal = sample(game.get_legal_moves(), width)
        if depth == 0 or not legal:
            return self.evaluate(game)
        else:
            utilities = []
            for move in legal:
                game.execute_move(move)
                utilities.append(self.explore(depth - 1, width, temp))
                game.undo_move(move)
            return max_by_key(player, utilities)


class ZeroSum(Evaluator):
    def __init__(self, *utility_funcs, **kwargs):
        self.utilities = utility_funcs
        super().__init__(**kwargs)

    def evaluate(self, game):
        utility = {}
        for func in self.utilities:
            utility.update(func(game))


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
