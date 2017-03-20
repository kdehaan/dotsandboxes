

class Dotgraph():
    #undirected graph to represent board state
    def __init__(self):
        self.elements = dict()
        self.elemValue = dict()
        self.elemType = dict()
        self.i = 0
        self.j = 0

    def add_element(self, key):
        if key in self.elements:
            raise RuntimeError("Bad argument:"
                               "Element {} already in the graph".format(key))
        self.elements[key] = list()

    def is_element(self, key):
        return key in self.elements

    def set_type(self, key, elemtype):
        self.elemType[key] = elemtype

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