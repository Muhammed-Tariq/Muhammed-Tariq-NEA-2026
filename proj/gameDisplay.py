import pygame as py
from gameLogic import Board

py.init()
screen = py.display.set_mode((600, 600), 0, 32)

# Constants

BOARD_LENGTH = 600
BOARD_HEIGHT = 600
SQUARES = 8

# Game loop

game = Board((0, 0), BOARD_LENGTH, BOARD_HEIGHT, py.Color("#00235c"), py.Color("#619dff"))
while True:
    screen.fill((255, 255, 255))
    Board.drawBoard(game, screen)
    py.display.flip()
    


