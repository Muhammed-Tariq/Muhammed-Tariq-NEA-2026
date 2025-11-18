import pygame as py

class Board():
    def __init__(self, position, length, height):
        self.board = [["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"], 
                      ["bP"] * 8,
                      [""] * 8,
                      [""] * 8,
                      [""] * 8,
                      [""] * 8,
                      ["wP"] * 8,
                      ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.moveHistory = []
        self.whiteToMove = True # True if White is to move, False if Black is to move
        self.position = position
        self.length = length
        self.height = height
        self.squareSize = length / 8


