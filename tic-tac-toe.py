#!/usr/bin/env python

from Tkinter import Tk
from game import Game

def start_game():
    game = Tk()
    game.title("Tic Tac Toe Game!")
    tictac_game = Game(game)
    game.mainloop()

if __name__ == '__main__':
    start_game()