from tkinter import *
from random_ai import RandomAi

class Display(Frame):

    def __init__(self, master, gboard):
        self.player = 'one'
        self.currentcolour = 'blue'
        # self.gametype = 'twoplayer'
        self.AI = RandomAi()
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

    def do_bot(self, AI):

        line = AI.play(self.gboard)
        if not line:
            print("no possible moves")
            return None
        else:
            self.update_board(line)
            self.canvas.itemconfig(line, fill="black")
            self.canvas.itemconfig(line, tags=("taken"))
            self.canvas.update_idletasks()



    def do(self, event, tag):
        self.update_board(tag)
        self.canvas.itemconfig("current", fill="black")
        # this tag for hovering, hover effects only work if "taken" is not present in the list of tags
        self.canvas.itemconfig("current", tags=("taken"))


    def update_board(self, tag):
        print("got here")
        self.gboard.set_value(tag, 1) #fill line on board
        additionalTurn = False
        for n in self.gboard.neighbours(tag):
            if self.gboard.filled_borders(n) == 4:
                additionalTurn = True
                self.gboard.filled_tiles = self.gboard.filled_tiles + 1
                print('filled ', n)
                i = int(n[4])
                j = int(n[5])
                self.canvas.create_rectangle(i*100+60, j*100+60,
                i*100+150, j*100+150, fill=self.currentcolour)
                self.gboard.set_value(n, self.player) #fill tile with whoever did it
        if not additionalTurn:
            self.switch_player()
        if self.gboard.check_filled():
            print('board is filled')
            score = self.gboard.check_score('one', 'two')
            if score[0] > score[1]:
                print('Player One wins with a score of',
                 score[0], 'to', score[1])
            else:
                print('Player Two wins with a score of',
                 score[1], 'to', score[0])





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
        starttag = "startbutton"
        self.canvas.create_rectangle(5, 5,
        40, 40, fill="red", tags=starttag)
        startcallback = lambda event, tag=starttag: self.do_bot(self.AI)
        self.canvas.tag_bind(starttag, '<Button-1>', startcallback)
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
