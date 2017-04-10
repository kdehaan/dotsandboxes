import random
import time

class StandardAi():
    def __init__(self):
        self.name = "StandardAi"# self.gboard = gboard

    def play(self, gboard, delay=0.15):
        time.sleep(delay)

        if gboard.safe_lines and gboard.primed_tiles:
            tile = random.choice(tuple(gboard.primed_tiles)) #take set element randomly
            for tileborder in gboard.neighbours(tile):
                if gboard.get_value(tileborder) == 0:
                    return tileborder

        if gboard.safe_lines:
            return random.choice(tuple(gboard.safe_lines))

        if gboard.primed_tiles:
            countOfTwo = 0
            potentialPlace = None
            for key in gboard.set_size:
                setSize = gboard.set_size[key]
                if setSize == 1:
                    tileborder = gboard.empty_set_borders(key)
                    if tileborder:
                        return tileborder
                if setSize == 2:
                    tileborder = gboard.empty_set_borders(key)
                    if tileborder:
                        countOfTwo = countOfTwo + 1
                        potentialPlace = tileborder
            # print(gboard.primed_tiles)
            if (countOfTwo == 1) and (len(gboard.primed_tiles) == 1):
                if gboard.filled_tiles == ((gboard.i-1)*(gboard.j-1)-2):
                    for tile in gboard.primed_tiles:
                        for tileborder in gboard.neighbours(tile):
                            if gboard.get_value(tileborder) == 0:
                                return tileborder
                return potentialPlace

            tile = random.choice(tuple(gboard.primed_tiles)) #take set element randomly
            for tileborder in gboard.neighbours(tile):
                if gboard.get_value(tileborder) == 0:
                    return tileborder

        if gboard.set_size:
            minset = min(gboard.set_size, key=gboard.set_size.get)
            for tileborder in gboard.neighbours(minset):
                if gboard.get_value(tileborder) == 0:
                    return tileborder
        else:
            return None






        # if gboard.primed_tiles:
        #     for key in gboard.set_size:
        #
        #         if gboard.set_size[key] == 1:
        #             for tileborder in gboard.neighbours(key):
        #                 if gboard.get_value(tileborder) == 0:
        #                     return tileborder
        #
        #         if gboard.set_size[key] == 2:
        #             if gboard.filled_tiles == ((gboard.i-1)*(gboard.j-1)-2):
        #                 for tile in gboard.primed_tiles:
        #                     for tileborder in gboard.neighbours(tile):
        #                         if gboard.get_value(tileborder) == 0:
        #                             return tileborder
        #
        #             tile_candidate = gboard.empty_set_borders(key)
        #             if tile_candidate:
        #                 return tile_candidate
        #
        #             else:
        #                 for tileborder in gboard.neighbours(key):
        #                     if gboard.get_value(tileborder) == 0:
        #                         return tileborder
        #
        # if gboard.set_size:
        #     minset = min(gboard.set_size, key=gboard.set_size.get)
        #     for tileborder in gboard.neighbours(minset):
        #         if gboard.get_value(tileborder) == 0:
        #             return tileborder
        #
        #
        # return None














        #     if gboard.set_size[minset] == 1:
        #
        #         (temptile,) =  gboard.set_map[minset] #you have found the irreproducable error, congrats
        #         for tileborder in gboard.neighbours(temptile):
        #             if gboard.get_value(tileborder) == 0:
        #                 return tileborder
        #     if gboard.set_size[minset] == 2:
        #         if gboard.filled_tiles == ((gboard.i-1)*(gboard.j-1)-2):
        #             for tile in gboard.primed_tiles:
        #                 for tileborder in gboard.neighbours(tile):
        #                     if gboard.get_value(tileborder) == 0:
        #                         return tileborder
        #
        #         tile_candidate = gboard.empty_set_borders(minset)
        #         if tile_candidate:
        #             return tile_candidate
        #         else:
        #             for tileborder in gboard.neighbours(minset):
        #                 if gboard.get_value(tileborder) == 0:
        #                     return tileborder
        #
        #
        # # print(gboard.set_size)
        # if gboard.set_size:
        #     for item in gboard.set_size:
        #         for tileborder in gboard.neighbours(item):
        #             if gboard.get_value(tileborder) == 0:
        #                 return tileborder
        # else:
        #     return None









    # def play(self, gboard, delay=0.15):
    #     time.sleep(delay)
    #     # print(gboard.safe_lines)
    #     # print(gboard.set_size)
    #     needsMoreData = False
    #     # print(gboard.set_size)
    #     if gboard.primed_tiles:
    #         for tile_candidate in gboard.primed_tiles:
    #             mainSet = gboard.get_set(tile_candidate)
    #             if gboard.set_size[mainSet] != 2:
    #                 # print(gboard.set_size)
    #                 tile = random.choice(tuple(gboard.primed_tiles)) #take set element randomly
    #                 for tileborder in gboard.neighbours(tile):
    #                     if gboard.get_value(tileborder) == 0:
    #                         # print(tileborder)
    #                         return tileborder
    #             else:
    #                 needsMoreData = True
    #                 # open_border = gboard.empty_set_borders(mainSet)
    #                 # if open_border:
    #                 #     return open_border
    #                 # else:
    #                 #     for tileborder in gboard.neighbours(tile_candidate):
    #                 #         if gboard.get_value(tileborder) == 0:
    #                 #             # print(tileborder)
    #                 #             return tileborder
    #
    #
    #     if gboard.safe_lines:
    #         return random.choice(tuple(gboard.safe_lines))
    #
    #     if needsMoreData:
    #         for tile_candidate in gboard.primed_tiles:
    #             open_border = gboard.empty_set_borders(gboard.get_set(tile_candidate))
    #             if gboard.filled_tiles == ((gboard.i-1)*(gboard.j-1)-2):
    #                 for tileborder in gboard.neighbours(tile_candidate):
    #                         if gboard.get_value(tileborder) == 0:
    #                             return tileborder
    #             if open_border:
    #                 return open_border
    #             else:
    #                 for tileborder in gboard.neighbours(tile_candidate):
    #                     if gboard.get_value(tileborder) == 0:
    #                         # print(tileborder)
    #                         return tileborder
    #
    #     try:
    #         minset = min(gboard.set_size, key=gboard.set_size.get)
    #     except ValueError:
    #         # print("board filled")
    #
    #         return None # no possible moves
    #     # print(gboard.set_size)
    #     for tileborder in gboard.neighbours(minset):
    #         if gboard.get_value(tileborder) == 0:
    #             # print(tileborder)
    #             return tileborder
