from tkinter import *
from random_ai import RandomAi
from standard_ai import StandardAi
from dotgraph import create_board

class Display(Frame):

    def __init__(self, master, gboard):
        self.board_sizes = (4, 5, 6, 7, 8, 9, 10, 11)
        self.bots = {"Random AI":RandomAi(), "Standard AI":StandardAi()} #none for now until i figure out how to add
        self.player = 'one'
        self.currentcolour = 'blue'
        self.p1wins = 0
        self.p2wins = 0
        self.games = 0
        self.master = master
        self.gametype = 'noplayer'
        self.AI = RandomAi() # self.AI also is the AI for human VS bot
        self.AI2 = RandomAi()

        self.gboard = gboard
        self.frame = Frame(master)
        self.frame.pack(fill="both", expand=True)
        self.c_width, self.c_height = self.gboard.i*100, self.gboard.j*100
        self.canvas = Canvas(self.frame, width=self.c_width, height=self.c_height)
        self.canvas.pack(fill="both", expand=True)
        self.frameb=Frame(self.frame)
        self.frameb.pack(fill="both", expand=True)
        master.title("Dots and Boxes")

        self.initBtns(master) #creates buttons for menu and instructions

        self.initUI(self.gboard.i, self.gboard.j)

    def switch_player(self):
        if self.player == 'one':
            self.player = 'two'
            self.currentcolour = 'red'
        else:
            self.player = 'one'
            self.currentcolour = 'blue'

        self.canvas.itemconfig(self.turn_indicator, fill = self.currentcolour)

    #used for game reset
    def reset(self, win, x_dots, y_dots, gamemode, AI1="Random AI", AI2="Random AI"):
        win.destroy() # close the menu window
        self.gboard = create_board(x_dots, y_dots)

        self.canvas.delete("all") # clear the old board and replace with a new board
        self.c_width, self.c_height = self.gboard.i*100, self.gboard.j*100
        self.canvas.config(width=self.c_width, height=self.c_height)

        self.AI = self.bots[AI1]
        self.AI2 = self.bots[AI2]

        self.gametype = gamemode
        self.player = 'one'
        self.currentcolour = 'blue'

        self.initUI(self.gboard.i, self.gboard.j)
        print("Game reset")

    def do_bot(self, AI):
        '''Uses the AI to play a turn for the both
        Returns True if a turn was taken, False if no possible moves exist'''
        line = AI.play(self.gboard, 0) #default delay is 0
        if not line:
            print("no possible moves")
            return False
        else:
            self.canvas.itemconfig(line, fill="black")
            self.canvas.itemconfig(line, tags=("taken"))
            self.canvas.update_idletasks()
            self.update_board(line)
            return True


    def do(self, event, tag):
        # only respond if at least one human player
        if self.gametype != "noplayer":
            self.canvas.itemconfig("current", fill="black")
            # this tag for hovering, hover effects only work if "taken" is not present in the list of tags
            self.canvas.itemconfig("current", tags=("taken"))
            self.update_board(tag)

        # if only one human player
        if self.gametype == 'oneplayer' and self.player == 'two':
            play_bot = True
            while play_bot: # allows for taking multiple turns as needed
                move_possible = self.do_bot(self.AI, 0.15)
                if self.player == 'one' or not move_possible:
                    play_bot = False

    #creates popup for end of game
    def game_over_alert(self, msg):
        alert = Toplevel()
        alert.title("Game Over")
        alert.resizable(width=False, height=False)

        Label(alert, text=msg).grid(row = 0, column = 0, columnspan=2)
        rst_btn = Button(alert, text='New Game', command=
                lambda: self.reset(alert, self.gboard.i, self.gboard.j, self.gametype))
        rst_btn.grid(row=1, column=0)

        ok_btn = Button(alert, text='Ok', command=alert.destroy)
        ok_btn.grid(row=1, column=1)

        alert.transient(self.master)
        alert.wait_visibility()
        alert.grab_set()
        self.master.wait_window(alert)

    def update_board(self, tag, visualize=True):
        self.gboard.set_value(tag, 1) #fill line on board
        if tag in self.gboard.safe_lines:
            self.gboard.safe_lines.remove(tag)
        additionalTurn = False
        for n in self.gboard.neighbours(tag):
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




        if not additionalTurn:
            self.switch_player()
        if self.gboard.check_filled():
            print('board is filled')
            score = self.gboard.check_score('one', 'two')
            if score[0] > score[1]:
                self.p1wins = self.p1wins + 1
                game_end_msg = 'Player One(Blue) wins with a score of \n{} to {}'.format(score[0], score[1])
            else:
                self.p2wins = self.p2wins + 1
                game_end_msg = 'Player Two(Red) wins with a score of \n{} to {}'.format(score[1], score[0])

            print(game_end_msg)
            self.game_over_alert(game_end_msg)



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
        # turn indicator
        self.canvas.create_text(100, 5, anchor="nw", text="Current Turn: ", font=("", 14))
        self.turn_indicator = self.canvas.create_rectangle(250, 5,
        275, 30, fill = self.currentcolour)

        # turn stepping button only for AI vs AI
        if self.gametype == "noplayer":
            starttag = "startbutton"
            self.canvas.create_rectangle(5, 5,
            40, 40, fill="white", tags=starttag)
            self.canvas.create_text((22, 22), text="STEP", font=("", 10), tags=starttag) # step button label
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


    def show_help(self):
        #show instructions and rules of play
        with open("instructions.txt", 'r') as help_file:
            help_info = help_file.read()
            help_win = Toplevel()
            help_win.title("HELP")
            help_win.resizable(width=False, height=False)

            help_text = Label(help_win, text=help_info, font=("", 20))
            help_text.pack()

            Button(help_win, text='Close', command=help_win.destroy).pack()

            help_win.transient(self.master)
            help_win.wait_visibility()
            help_win.grab_set()
            self.master.wait_window(help_win)

    def initBtns(self, master):
        #adds buttons to the main window(witht he board) for opening instructions and the menu
        self.menu_btn = Button(self.frameb, text='Menu', command=lambda: self.menu_confirm(master))
        self.menu_btn.grid(row=0, column=1, padx=15)
        help_btn = Button(self.frameb, text='Help', command=self.show_help)
        help_btn.grid(row=0, column=2, padx=15)
        self.frameb.grid_columnconfigure(0, weight=1)
        self.frameb.grid_columnconfigure(3, weight=1)

#--- MENU ---#
    def initMenu(self, master):
        menu_win = Toplevel()
        menu_win.title("MENU")
        menu_win.resizable(width=False, height=False)

        Label(menu_win, text="Start new game with these settings: ").grid(row = 0, column = 0)
        rst_btn = Button(menu_win, text='Reset', command=
                lambda: self.reset(menu_win, b_width.get(), b_height.get(), gamemode.get().lower().replace(" ", ""),
                bot1.get(), bot2.get()))
        rst_btn.grid(row=0, column=1)

        #board size
        Label(menu_win, text="Board width: ").grid(row = 1, column = 0)
        b_width = IntVar()
        b_width.set(self.gboard.i)
        b_width_options = OptionMenu(menu_win, b_width, *self.board_sizes)
        b_width_options.grid(row = 1, column = 1)
        Label(menu_win, text="Board height: ").grid(row = 2, column = 0)
        b_height = IntVar()
        b_height.set(self.gboard.j)
        b_height_options = OptionMenu(menu_win, b_height, *self.board_sizes)
        b_height_options.grid(row = 2, column = 1)

        #player settings
        Label(menu_win, text="Number of players: ").grid(row = 3, column = 0)
        gamemode = StringVar()
        gamemode.set(self.gametype.replace('p', ' p'))
        gamemode_options = OptionMenu(menu_win, gamemode, "One Player", "Two Player", "No Player")
        gamemode_options.grid(row = 3, column = 1)

        #AI settings
        Label(menu_win, text="First AI(Used for one player only games): ").grid(row=4, column = 0)
        bot1 = StringVar()
        bot1.set("Random AI")
        bot1_options = OptionMenu(menu_win, bot1, *self.bots.keys())
        bot1_options.grid(row=4, column=1)

        Label(menu_win, text="Second AI(Used AI vs AI games): ").grid(row=5, column = 0)
        bot2 = StringVar()
        bot2.set("Random AI")
        bot2_options = OptionMenu(menu_win, bot2, *self.bots.keys())
        bot2_options.grid(row=5, column=1)

        menu_win.transient(master)
        menu_win.wait_visibility()
        menu_win.grab_set()
        master.wait_window(menu_win)

    def goto_menu(self, master, confirm_window):
        confirm_window.destroy()
        print("Menu")
        # remove menu button from other window
        # self.menu_btn.destroy()
        self.initMenu(master) # opens menu window?

    def menu_confirm(self, master):
        # create child window
        win = Toplevel()
        win.title("Confirm")
        # display message
        message = "Do you want to go to the menu?(Game progress is lost upon reset)"
        Label(win, text=message).pack()
        Button(win, text='Yes', command=lambda: self.goto_menu(master, win)).pack()
        Button(win, text='No', command=win.destroy).pack()

        win.transient(master)
        win.wait_visibility()
        win.grab_set()
        master.wait_window(win)
#--- End of MENU ---#

def main():
    root=Tk()
    app=Display(root)
    root.mainloop()
    # gboard = create_board(6, 6)

if __name__ == '__main__':
    main()
