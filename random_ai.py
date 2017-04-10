import random
import time

class RandomAi():
    def __init__(self):
        self.name = "RandomAi"# self.gboard = gboard

    def play(self, gboard, delay=0.15):
        time.sleep(delay)
        # print(gboard.safe_lines)
        # print(gboard.set_size)
        if gboard.primed_tiles:
            # print(gboard.set_size)
            tile = random.choice(tuple(gboard.primed_tiles)) #take set element randomly
            for tileborder in gboard.neighbours(tile):
                if gboard.get_value(tileborder) == 0:
                    # print(tileborder)
                    return tileborder

        if gboard.safe_lines:
            return random.choice(tuple(gboard.safe_lines))


        if gboard.set_size:
            minset = min(gboard.set_size, key=gboard.set_size.get)
            for tileborder in gboard.neighbours(minset):
                if gboard.get_value(tileborder) == 0:
                    # print(tileborder)
                    return tileborder
        else:
            return None


        # try:
        #     minset = min(gboard.set_size, key=gboard.set_size.get)
        # except ValueError:
        #     # print("board filled")
        #     return None # no possible moves
        # # print(gboard.set_size)
        # for tileborder in gboard.neighbours(minset):
        #     if gboard.get_value(tileborder) == 0:
        #         # print(tileborder)
        #         return tileborder
