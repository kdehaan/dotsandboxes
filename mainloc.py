from dotgraph import Dotgraph, create_board
from display2 import Display
from tkinter import Tk


def main():
    gboard = create_board(6, 6)
    root=Tk()
    app=Display(root, gboard)
    root.mainloop()


if __name__ == '__main__':
    main()
