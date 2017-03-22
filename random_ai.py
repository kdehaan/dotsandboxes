import random
import time

class RandomAi():
    def __init__(self):
        self.name = "RandomAi"# self.gboard = gboard

    def play(self, gboard):
        time.sleep(0.15)
        if gboard.three_tiles:
            tile = gboard.three_tiles.pop()
            borderlist = gboard.neighbours(tile)
            random.shuffle(borderlist)
            for border in borderlist:
                if gboard.get_value(border) is not 1:
                    return border
        elif gboard.oneorzero_tiles:
            tile = gboard.oneorzero_tiles.pop()
            borderlist = gboard.neighbours(tile)
            random.shuffle(borderlist)
            for border in borderlist:
                if gboard.get_value(border) is not 1:
                    otherTile = gboard.other_tile(tile, border)
                    if otherTile == None:
                        return border
                    if otherTile not in gboard.two_tiles:
                        return border
                    continue
                    
        elif gboard.two_tiles:
            tile = gboard.two_tiles.pop()
            borderlist = gboard.neighbours(tile)
            random.shuffle(borderlist)
            for border in borderlist:
                if gboard.get_value(border) is not 1:
                    return border
        return None
