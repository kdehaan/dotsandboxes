from tkinter import *
from random_ai import RandomAi
from standard_ai import StandardAi
import dotgraph

class Display(Frame):

    def __init__(self, master, gboard):
        self.player = 'one'
        self.currentcolour = 'blue'
        self.p1wins = 0
        self.p2wins = 0
        self.games = 0
        # self.gametype = 'twoplayer'
        self.AI = StandardAi()
        # self.AI = RandomAi()
        self.AI1 = RandomAi()
        self.AI2 = StandardAi()
        # self.AI2 = RandomAi()
        self.gboard = gboard
        self.frame = Frame(master)
        self.frame.pack(fill="both", expand=True)
        self.canvas = Canvas(self.frame, width=600, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.frameb=Frame(self.frame)
        self.frameb.pack(fill="both", expand=True)
        self.initUI(self.gboard.i, self.gboard.j)

    def switch_player(self):
        if self.player == 'one':
            self.player = 'two'
            self.currentcolour = 'red'
        else:
            self.player = 'one'
            self.currentcolour = 'blue'

    def reset_board(self):
        i = self.gboard.i
        j = self.gboard.j
        self.gboard = dotgraph.create_board(i, j)
        self.initUI(self.gboard.i, self.gboard.j)

    def do_bots(self, AI1, AI2, count=1000):
        while count > self.games:
            print(self.games, end='\r')
            line = AI1.play(self.gboard, 0)
            if not line:
                self.reset_board()
                # print("no possible moves")
            else:
                self.update_board(line, False)
                # self.canvas.itemconfig(line, fill="black")
                # self.canvas.itemconfig(line, tags=("taken"))
                # self.canvas.update_idletasks()
            line = AI2.play(self.gboard, 0)
            if not line:
                self.reset_board()
                # print("no possible moves")
            else:
                self.update_board(line, False)
                # self.canvas.itemconfig(line, fill="black")
                # self.canvas.itemconfig(line, tags=("taken"))
                # self.canvas.update_idletasks()

        print('total wins: P1 -', self.p1wins, 'P2 -', self.p2wins)
        self.games = 0
        self.p1wins = 0
        self.p2wins = 0


    def do_bot(self, AI):

        line = AI.play(self.gboard, 0)

        if not line:
            print("no possible moves")
            return None
        else:

            self.update_board(line)
            self.canvas.itemconfig(line, fill='black')
            self.canvas.itemconfig(line, tags=("taken"))
            self.canvas.update_idletasks()



    def do(self, event, tag):
        self.update_board(tag)
        self.canvas.itemconfig("current", fill="black")
        # this tag for hovering, hover effects only work if "taken" is not present in the list of tags
        self.canvas.itemconfig("current", tags=("taken"))


    def display_sets(self):
        for i in range(self.gboard.i):
            for j in range(self.gboard.j):
                temptag = 'tile' + str(i) + str(j)
                self.canvas.create_text(i*100+100, j*100+100,
                text = self.gboard.get_set(temptag), fill="black")

    def update_board(self, tag, visualize=True):

        self.gboard.set_value(tag, 1) #fill line on board
        if tag in self.gboard.safe_lines:
            self.gboard.safe_lines.remove(tag)
        additionalTurn = False
        # needs_cleaning = False
        for n in self.gboard.neighbours(tag): # n is nearby tile

            i = int(n[4])
            j = int(n[5])
            n_borders = self.gboard.filled_borders(n)

            if n_borders == 2:
                review_sets = True
                self.gboard.create_set(n)
                for n_neighbour in self.gboard.neighbours(n):
                    if self.gboard.get_value(n_neighbour) == 0:
                        adjacent = self.gboard.other_tile(n, n_neighbour)
                        if self.gboard.in_set(adjacent):
                            adj_set = self.gboard.get_set(adjacent)
                            self_set = self.gboard.get_set(n)
                            #add smaller set to larger set
                            if self.gboard.set_size[adj_set] >= self.gboard.set_size[self_set]:
                                self.gboard.union_sets(adj_set, self_set)
                            else:
                                self.gboard.union_sets(self_set, adj_set)

                ###### TESTING
                if visualize:
                    # self.display_sets()
                    self.canvas.create_text(i*100+100, j*100+100,
                    text = self.gboard.get_set(n), fill=self.currentcolour)
                ###### TESTING
            if n_borders == 3:
                self.gboard.primed_tiles.add(n)
                self.gboard.sever_sets(tag)
            if n_borders == 4:
                self.gboard.primed_tiles.remove(n)
                additionalTurn = True
                self.gboard.filled_tiles = self.gboard.filled_tiles + 1
                self.gboard.set_value(n, self.player) #fill tile with whoever did it
                # self.gboard.sever_sets(tag)
                self.gboard.clean_set(n)#tidy up set



                if visualize:
                    self.canvas.create_rectangle(i*100+60, j*100+60,
                    i*100+150, j*100+150, fill=self.currentcolour)



        # print(self.gboard.set_map)

        if not additionalTurn:
            self.switch_player()
        if self.gboard.check_filled():
            # print('board is filled')
            self.games = self.games + 1
            score = self.gboard.check_score('one', 'two')
            if score[0] > score[1]:
                # print('Player One wins with a score of',
                #  score[0], 'to', score[1])
                self.p1wins = self.p1wins + 1
            else:
                # print('Player Two wins with a score of',
                #  score[1], 'to', score[0])
                self.p2wins = self.p2wins + 1
            # print('Current wins: P1 -', self.p1wins, 'P2 -', self.p2wins)





    def hover_on(self, event):
        if "taken" not in self.canvas.gettags("current"):
            self.canvas.itemconfig("current", fill="grey")

    def hover_off(self, enter):
        if "taken" not in self.canvas.gettags("current"):
            self.canvas.itemconfig("current", fill="white")

    # def do_update(self, event):
    #     print(event.widget.find_withtag("current"))
    #

    def initUI(self, xdots=5, ydots=5):

        #bot stepper
        startbot = "startbutton"
        self.canvas.create_rectangle(5, 5,
        40, 40, fill="red", tags=startbot)
        startcallback = lambda event, tag=startbot: self.do_bot(self.AI)
        self.canvas.tag_bind(startbot, '<Button-1>', startcallback)

        #bot fight
        startbots = "startbothbutton"
        self.canvas.create_rectangle(50, 5,
        85, 40, fill="orange", tags=startbots)
        startcallback = lambda event, tag=startbots: self.do_bots(self.AI1, self.AI2)
        self.canvas.tag_bind(startbots, '<Button-1>', startcallback)

        #reset the board

        resetboard = "resetbutton"
        self.canvas.create_rectangle(95, 5,
        130, 40, fill="purple", tags=resetboard)
        startcallback = lambda event, tag=resetboard: self.reset_board()
        self.canvas.tag_bind(resetboard, '<Button-1>', startcallback)


        for i in range(xdots):
            for j in range(ydots):
                self.canvas.create_rectangle(i*100+50, j*100+50, i*100+60, j*100+60,
                fill="black") #
                # self.canvas.tag_bind("dot" + str(dotNumber), '<Button-1>', self.do)
        for i in range(xdots-1):
            for j in range(ydots):
                self.canvas.create_rectangle(i*100+60, j*100+50, i*100+150, j*100+60,
                fill="white", outline="black", tags="horiz" + str(i)+str(j))

                tag = "horiz" + str(i)+str(j)
                callback = lambda event, tag=tag: self.do(event, tag)
                self.canvas.tag_bind(tag, '<Button-1>', callback)
                # self.canvas.tag_bind("horiz" + str(i)+str(j), '<Button-1>',
                # self.do)

                self.canvas.tag_bind("horiz" + str(i)+str(j), "<Enter>", self.hover_on)
                self.canvas.tag_bind("horiz" + str(i)+str(j), "<Leave>", self.hover_off)


        for i in range(xdots):
            for j in range(ydots-1):
                self.canvas.create_rectangle(i*100+50, j*100+60, i*100+60, j*100+150,
                fill="white", outline="black", tags="vert" + str(i)+str(j))

                tag = "vert" + str(i)+str(j)
                callback = lambda event, tag=tag: self.do(event, tag)
                self.canvas.tag_bind(tag, '<Button-1>', callback)

                self.canvas.tag_bind("vert" + str(i)+str(j), "<Enter>", self.hover_on)
                self.canvas.tag_bind("vert" + str(i)+str(j), "<Leave>", self.hover_off)


def main():
    root=Tk()
    app=Display(root)
    root.mainloop()
    # gboard = create_board(6, 6)

if __name__ == '__main__':
    main()
