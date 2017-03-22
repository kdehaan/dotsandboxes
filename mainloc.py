from dotgraph import Dotgraph, create_board
from display import Display
from tkinter import Tk


def main():
    gboard = create_board(10, 7)
    root=Tk()
    app=Display(root, gboard)
    root.mainloop()


if __name__ == '__main__':
    main()
