

class Dotgraph():
    #undirected graph to represent board state
    def __init__(self):
        self.elements = dict()
        self.elemValue = dict()
        self.elemType = dict()
        self.list_tiles = list()
        self.list_lines = list()
        self.i = 0
        self.j = 0
        self.filled_tiles = 0
        self.safe_lines = set()
        self.primed_tiles = set()
        self.set_map = dict() # points to tile in set
        self.tile_map = dict() # points to set of tile
        self.set_size = dict()

    def add_element(self, key):
        if key in self.elements:
            raise RuntimeError("Bad argument:"
                               "Element {} already in the graph".format(key))
        self.elements[key] = list()

    def is_element(self, key):
        return key in self.elements

    def create_set(self, key):
        self.set_size[key] = 1
        self.set_map[key] = set()
        self.set_map[key].add(key)
        self.tile_map[key] = key
        for border in self.neighbours(key):
            if border in self.safe_lines:
                self.safe_lines.remove(border)

    def union_sets(self, key, setname):
        if key != setname:
            self.set_map[key] = self.set_map[key] | self.set_map[setname]
            for item in self.set_map[setname]:
                self.tile_map[item] = key
            del self.set_map[setname]
            self.tile_map[setname] = key
            self.set_size[key] = self.set_size[key] + self.set_size.pop(setname)

    def in_set(self, key):
        if key in self.tile_map:
            return True
        return False

    def get_set(self, key):
        if key == None:
            return None
        if key not in self.tile_map:
            return None
        return self.tile_map[key]

    def clean_set(self, key):
        parentSet = self.get_set(key)
        if key == parentSet:
            self.set_map[key].remove(key)
            if not self.set_map[key]:
                del self.set_map[key]
                del self.set_size[key]
                return
            newSet = self.set_map[key].pop()
            self.set_map[newSet] = self.set_map[key]
            self.set_map[newSet].add(newSet)
            for item in self.set_map[newSet]:
                self.tile_map[item] = newSet
            self.set_size[newSet] = self.set_size[key] - 1
            del self.set_size[key]
            del self.set_map[key]

        else:
            self.set_map[parentSet].remove(key)
            self.set_size[parentSet] = self.set_size[parentSet] - 1

        del self.tile_map[key]


    def set_type(self, key, elemtype):
        self.elemType[key] = elemtype
        if elemtype == "tile":
            self.list_tiles.append(key)
        else:
            self.list_lines.append(key)
            self.safe_lines.add(key)

    def empty_set_borders(self, key):
        foundBorders = 0
        openBorder = None
        for item in self.set_map[key]:
            for border in self.neighbours(item):
                if self.get_value(border) == 0:
                    if self.get_set(self.other_tile(item, border)) != key:
                        openBorder = border
                        foundBorders = foundBorders + 1
        if foundBorders == 1:
            return openBorder
        else:
            return None

    def sever_sets(self, key): #key is a border
        adjacentTiles = list(self.neighbours(key))
        if len(adjacentTiles) != 2:
            del adjacentTiles #cleanup
            return
        tile1 = adjacentTiles[0]
        tile2 = adjacentTiles[1]
        set1 = self.get_set(tile1)
        set2 = self.get_set(tile2)
        # print(tile1, tile2, set1, set2)
        del adjacentTiles #cleanup
        if set1 != set2:
            return
        if set1 not in self.connected_tiles(tile1):
            newKey = tile1
            otherKey = tile2
        else:
            newKey = tile2
            otherKey = tile1
        # print(newKey, otherKey)
        otherSet = self.get_set(otherKey)

        connectedTiles = self.connected_tiles(newKey)
        for tile in connectedTiles: #update set mapping
            self.tile_map[tile] = newKey
            if tile in self.set_map[otherSet]:
                self.set_map[otherSet].remove(tile)

        self.set_map[newKey] = connectedTiles
        changeLen = len(connectedTiles)
        self.set_size[newKey] = changeLen
        self.set_size[otherSet] = self.set_size[otherSet] - changeLen
        if not self.set_map[otherSet]:
            del self.set_map[otherSet]


    def connected_tiles(self, key):
        tileset = set()
        tileset.add(key)
        tempkey = key
        moreToFind = True
        while moreToFind:
            moreToFind = False
            # print(tempkey, '------')
            for border in self.neighbours(tempkey):
                if self.get_value(border) == 0:
                    othertile = self.other_tile(tempkey, border)
                    if not self.in_set(othertile):
                        continue
                    if (othertile not in tileset) and othertile:
                        moreToFind = True
                        tileset.add(othertile)
                        tempkey = othertile
                        break
        return tileset




    def other_tile(self, tile, edge):
        for item in self.neighbours(edge):
            if item is not tile:
                return item
        return None

    def get_type(self, key):
        return self.elemType[key]

    def set_value(self, key, value):
        self.elemValue[key] = value

    def get_value(self, key):
        return self.elemValue[key]

    def add_edge(self, e):
        #e is a tuple of two element keys
        #careful not to connect twice
        if not self.is_element(e[0]):
            return
            # raise RuntimeError("Attempt to create an edge with"
            #                    "non-existent element: {}".format(e[0]))
        if not self.is_element(e[1]):
            return
            # raise RuntimeError("Attempt to create an edge with"
            #                    "non-existent element: {}".format(e[1]))

        self.elements[e[0]].append(e[1])
        self.elements[e[1]].append(e[0])

    def neighbours(self, key):
        return self.elements[key]

    def get_elements(self):
        return set(self.elements.keys())


    def filled_borders(self, key):
        filled = 0
        for border in self.neighbours(key):
            filled = filled + self.get_value(border)
        return filled


    def check_filled(self):
        if (self.i-1)*(self.j-1) == self.filled_tiles:
            return True
        return False

    def check_score(self, player_one, player_two):
        p1score = 0
        p2score = 0
        for item in self.list_tiles:
            if self.elemValue[item] == player_one:
                p1score = p1score + 1
            else:
                p2score = p2score + 1
        return [p1score, p2score]

def create_board(idots, jdots):
    board = Dotgraph()
    board.i = idots
    board.j = jdots
    for i in range(idots-1):
        for j in range(jdots):
            elemName = 'horiz'+str(i)+str(j)
            board.add_element(elemName)
            board.set_value(elemName, 0)
            board.set_type(elemName, 'line')
    for i in range(idots):
        for j in range(jdots-1):
            elemName = 'vert'+str(i)+str(j)
            board.add_element(elemName)
            board.set_value(elemName, 0)
            board.set_type(elemName, 'line')
    for i in range(idots-1):
        for j in range(jdots-1):
            elemName = 'tile'+str(i)+str(j)
            board.add_element(elemName)
            board.set_value(elemName, 0)
            board.set_type(elemName, 'tile')
            board.add_edge((elemName, ('vert'+str(i)+str(j))))
            board.add_edge((elemName, ('vert'+str(i+1)+str(j))))
            board.add_edge((elemName, ('horiz'+str(i)+str(j))))
            board.add_edge((elemName, ('horiz'+str(i)+str(j+1))))
    return board
