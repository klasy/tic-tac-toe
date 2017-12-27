#!/usr/bin/env python

from Tkinter import Label, Button, Radiobutton, IntVar, W, E, StringVar
import tkMessageBox

from random import choice

from board import Board
from player import Player


class Game:

    """
    This is our Game - everything important is handled here
    """

    def __init__(self, parent):
        self.parent = parent
        self.level = 1

        # create a board
        self.board = Board(self.parent, 100, "#ECECEC")  # hex color gray
        self.board.draw_board()

        # create players
        self.player1 = Player("Human")
        self.player2 = Player("Computer")

        self.level_var = IntVar()

        # setting the player to Human as the Human starts
        self.player = self.player1

        self.initialize_controls()
        self.layout()

    def initialize_controls(self, rest=False):
        label_text = StringVar()
        label_text.set("It is a %s's turn" % self.player.name)
        self.board.canvas.bind('<Button-1>', self.move)

        self.label = Label(self.board.container,
                           textvariable=label_text)
        self.level1 = Radiobutton(self.board.container,
                                  text="Easy",
                                  variable=self.level_var,
                                  value=1,
                                  command=self.update_level)
        self.level2 = Radiobutton(self.board.container,
                                  text="Medium",
                                  variable=self.level_var,
                                  value=2,
                                  command=self.update_level)
        self.level3 = Radiobutton(self.board.container,
                                  text="Hard",
                                  variable=self.level_var,
                                  value=3,
                                  command=self.update_level)
        self.reset_button = Button(self.board.container,
                                   text="Reset",
                                   width=25,
                                   command=self.restart)

    def layout(self):
        # register buttons to board's container
        self.label.grid()
        self.level1.grid(row = 0, column = 1, sticky = W)
        self.level2.grid(row = 1, column = 1, sticky = W)
        self.level3.grid(row = 2, column = 1, sticky = W)
        self.level_var.set(self.level)
        self.reset_button.grid(row = 4, sticky = E)

    def update_level(self):
        self.level = self.level_var.get()

    def restart(self):
        ''' Restart the game from the very beginning, reinitialize everything '''
        self.board.container.destroy()
        self.player1.clean_moves()
        self.player2.clean_moves()

        self.board = Board(self.parent, 100, "#ECECEC")
        self.board.draw_board()
        self.player = self.player1
        self.initialize_controls(rest=True)
        self.layout()

    def move(self, event):
        """
        This method is called when the button is clicked
        :param event: this is a mouse click with coordinates
        """

        if self.player.name == "Computer":
            self.computers_move()
        else:
            self.humans_move(event)

    def computers_move(self):

        xy_key = self.make_a_move(self.level)

        if xy_key is None:
            # something went wrong
            # need to handle it correctly
            self.result("We can't make a move any more!", "error")
            return

        x, y = self.board.translate_cells_dict_key_to_text_coords(xy_key)
        self.board.canvas.create_text(x, y, text="O", font=("Purisa", 60))

        # update the unused cells dictionary
        self.player.add_move(self.board.unused_cells_dict[xy_key])
        self.board.update_unused_cells_dict(xy_key)

        if self.check_if_won():
            return

        self.player = self.player1

    def humans_move(self, event):
        """
        This function handles
        :param event: this is a click event
        """

        if len(self.board.get_unused_cells_dict()) == 0:
            self.result("The game is over! Click Reset button", "info")
            return

        # a little logic to get the top left corner coords to draw the text
        floor_x, floor_y = self.board.get_floor_coord(event.x, event.y)
        xy_key = self.board.convert_coord_to_key(floor_x, floor_y)

        if not self.board.check_if_key_available(xy_key):
            self.result("This cell is already busy - please, make another move", "warning")
            return

        x, y = self.board.translate_cells_dict_key_to_text_coords(xy_key)
        self.board.canvas.create_text(x, y, text="X", font=("Purisa", 60))

        # update the unused cells dictionary
        self.player.add_move(self.board.unused_cells_dict[xy_key])
        self.board.update_unused_cells_dict(xy_key)

        if self.check_if_won():
            return

        self.player = self.player2

        # imitate a button click for a computer move
        # with the event = None
        self.move(None)

    def make_a_move(self, level):
        """
        Here we make a move according to the computer intelligence level
        """

        unused_cells = self.board.get_unused_cells_dict()
        # if there's no more unused cells left
        # we can't move
        if len(unused_cells) == 0:
            return None

        cell_key = ""

        cells_list = unused_cells.keys()
        if level == 1:
            cell_key = choice(cells_list)
        if level == 3:
            # if it is the first move
            if len(unused_cells) == 8:
                corner_values = [1, 3, 7, 9]
                # if the first move was made in the corner
                if any(x in corner_values for x in self.player1.moves):
                    return "11"
                # else if the center field is taken
                elif "11" not in unused_cells.keys():
                    tmp_unused_cells = {item.key:item.value for item in unused_cells if item.value() in corner_values}
                    return choice(tmp_unused_cells.keys())
        if level == 2 or level == 3:
            # check if there's any pair where we can win
            tmp_cell_key_computer = self.check_twos(self.player2)
            if tmp_cell_key_computer == []:
                # if there's no such pair we need to prevent human from winning
                tmp_cell_key_human = self.check_twos(self.player1)
                if tmp_cell_key_human == []:
                    cell_key = choice(cells_list)
                else:
                    cell_key = choice(tmp_cell_key_human)
            else:
                cell_key = choice(tmp_cell_key_computer)

        return cell_key

    def check_twos(self, player):
        result_list = []
        for item in self.board.winning_combos:
            tmp_twos_dict = [[item[1], item[2]],
                             [item[0], item[2]],
                             [item[0], item[1]]]
            if tmp_twos_dict[0][0] in player.moves and tmp_twos_dict[0][1] in player.moves:
                result_list.append(item[0])
            if tmp_twos_dict[1][0] in player.moves and tmp_twos_dict[1][1] in player.moves:
                result_list.append(item[1])
            if tmp_twos_dict[2][0] in player.moves and tmp_twos_dict[2][1] in player.moves:
                result_list.append(item[2])
        result_keys = self.board.convert_vals_to_keys(result_list)
        return result_keys

    def check_if_won(self):
        ''' Here we define if the current user wins the game or is t a tie '''

        # if we did not do the 3 moves yet we could not have won
        if len(self.player.moves) < 3:
            return False

        for combo in self.board.winning_combos:
            if combo[0] in self.player.moves and \
               combo[1] in self.player.moves and \
               combo[2] in self.player.moves:
                self.result("%s wins!" % self.player.name, "info")
                self.board.unused_cells_dict = {}
                return True

        if len(self.board.get_unused_cells_dict()) == 0:
            self.result("It's a TIE!!!!", "info")
            return True

    def result(self, text, show_opt):
        ''' This function is gonna show the message box above the board '''
        if show_opt == "info":
            tkMessageBox.showinfo(title="Congraulations!", message=text)
        elif show_opt == "warning":
            tkMessageBox.showwarning(title="Warning!", message=text)
        elif show_opt == "error":
            tkMessageBox.showerror(title="Error!!!", message=text)