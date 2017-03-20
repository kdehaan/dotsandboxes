import random

class RandomAi():
    def __init__(self):
        self.name = "RandomAi"# self.gboard = gboard

    def play(self, gboard):
        if gboard.three_tiles:
            tile = gboard.three_tiles.pop()
            for border in gboard.neighbours(tile):
                if gboard.get_value(border) is not 1:
                    return border
        elif gboard.oneorzero_tiles:
            tile = gboard.oneorzero_tiles.pop()
            for border in gboard.neighbours(tile):
                if gboard.get_value(border) is not 1:
                    return border
        elif gboard.two_tiles:
            tile = gboard.two_tiles.pop()
            for border in gboard.neighbours(tile):
                if gboard.get_value(border) is not 1:
                    return border
        return None
