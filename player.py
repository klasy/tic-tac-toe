#!/usr/bin/env python

import random

class Player:
    """
    This is the class to create and identify our players.

    Attributes:
        name - the property to identify the user (i.e. user1, computer, etc)
    """

    def __init__(self, name):
        self.name = name
        self.moves = []

    def add_move(self, cell_number):
        self.moves.append(cell_number)

    def clean_moves(self):
        self.moves = []