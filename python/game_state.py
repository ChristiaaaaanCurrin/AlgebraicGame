

class GameState:
    def __init__(self, game=None, **kwargs):
        self.game = game
        self.items = kwargs

    def __repr__(self):
        return f'State: {self.game}, {self.items}'

    def __str__(self):
        return str(self.items)

    def __getitem__(self, item):
        return self.items[item]

    def __setitem__(self, key, value):
        self.items.update(**{key: value})

    def key_intersection(self, *keys):
        """
        :param keys: correspond with keys for self.items
        :return: list of items that are in all lists keyed by one of keys; returns empty list if no keys are given
        """
        if keys:
            start, *keys = keys
            items = self.items[start]
            for key in keys:
                items = filter(lambda item: item in self[key], items)
            return items
        else:
            return []

    def key_union(self, *keys):
        """
        :param keys: correspond with keys for self.items
        :return: list of items that are in any lists keyed by one of keys
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
