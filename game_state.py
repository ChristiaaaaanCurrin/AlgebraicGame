

class GameState:
    def __init__(self, game=None, **kwargs):
        self.game = game
        self.items = kwargs

    def __repr__(self):
        return f'State: {self.game}, {self.items}'

    def __str__(self):
        return str(self.items)

    def __getitem__(self, item):
        try:
            return self.items[item]
        except KeyError:
            self.items[item] = None
            return None

    def __setitem__(self, key, value):
        self.items.update(**{key: value})

    def key_intersection(self, *keys):
        """
        :param keys: correspond with keys for self.items
        :return: list of rules that are in all bins keyed by one of keys or all top rules if no keys are given
        """
        if keys:
            start, *keys = keys
            items = self.items[start]
            for key in keys:
                items = filter(lambda r: key in r.keys, items)
            return items
        else:
            items = []
            [items.extend(rules) for rules in self.items.values()]
            return items

    def key_union(self, *keys):
        """
        :param keys: correspond with keys for self.items
        :return: list of items that are in any bins keyed by one of keys
        """
        items = []
        for key in keys:
            if key in self.items:
                for item in self.items[key]:
                    if item not in items:
                        items.append(item)
        return items


if __name__ == "__main__":
    gs = GameState(None)
