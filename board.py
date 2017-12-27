#!/usr/bin/env python

from Tkinter import Frame, Canvas, W, E, N, S

CELLS_DICT = {'00': 1, '10': 2, '20': 3,
              '01': 4, '11': 5, '21': 6,
              '02': 7, '12': 8, '22': 9}

WINNING_COMBOS = [(1, 2, 3), (4, 5, 6), (7, 8, 9),
                  (1, 4, 7), (2, 5, 8), (3, 6, 9),
                  (1, 5, 9), (3, 5, 7)]

class Board:
    """
    This is our board for the game
    """

    def __init__(self, parent, size, color):
        self.parent = parent
        self.size = size
        self.color = color

        # design to fit tkinter grid(row, col)two params
        self.unused_cells_dict = CELLS_DICT.copy()

        # creating main container for the board
        self.container = Frame(self.parent)
        self.container.pack()

        # creating canvas for the container
        self.canvas = Canvas(self.container,
                             width = self.size * 3,
                             height = self.size * 3)
        self.canvas.grid(row = 0, column = 0, rowspan=3, sticky=W+E+N+S)

    def draw_board(self):
        ''' Draw the board '''
        for row in xrange(3):
            for col in xrange(3):
                self.canvas.create_rectangle(self.size * col,
                                             self.size * row,
                                             self.size * (col + 1),
                                             self.size * (row + 1),
                                             fill = self.color)

    def get_unused_cells_dict(self):
        return self.unused_cells_dict

    def update_unused_cells_dict(self, key):
        ''' Remove used key from the dictionary '''
        self.unused_cells_dict.pop(key)

    def check_if_key_available(self, key):
        if not key in self.unused_cells_dict.keys():
            return False
        return True

    def reset_unused_cells_dict(self):
        self.unused_cells_dict = CELLS_DICT.copy()

    def get_event_coord(self, e):
        ''' Get the event coordinates '''
        return e.x, e.y

    def get_floor_coord(self, col, row):
        floor_col = col // self.size
        floor_row = row // self.size
        return floor_col, floor_row

    def convert_coord_to_key(self, col, row):
        return str(col) + str(row)

    def get_selected_cell_coords(self, event):
        """
        finding coordinates of a cell in a 9-cell grid
        :param event: this should be triggered by a user click
        :return: tuple of column and row
        """

        col, row = self.get_event_coord(event)
        floor_col, floor_row = self.get_floor_coord(col, row)

        corner_col = floor_col * self.size + self.size
        corner_row = floor_row * self.size + self.size

        return corner_col, corner_row

    def translate_cells_dict_key_to_text_coords(self, key):
        """
        This function will get the top left corner of the rectangle coordinates
        to enable us to draw the text in the right rectangle
        :param key: is a key in the CELLS_DICT
        :return: x & y of the top left corner of the rectangle
        """
        x_key = int(key[0])
        y_key = int(key[1])

        x = x_key * self.size + self.size/2
        y = y_key * self.size + self.size/2

        return x, y

    def convert_vals_to_keys(self, res):
        ret_keys = []
        for i in res:
            if i not in self.unused_cells_dict.values():
                continue
            for key, value in CELLS_DICT.iteritems():
                if value == i:
                    ret_keys.append(key)
        return ret_keys

    @property
    def winning_combos(self):
        return WINNING_COMBOS