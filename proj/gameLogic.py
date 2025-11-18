import pygame as py

class Board():
    def __init__(self, position, length, height, darkCol, lightCol):
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
        self.darkCol = darkCol
        self.lightCol = lightCol

    def drawBoard(self, screen, codes, images):
        x = 0 + self.position[0]
        y = 0 + self.position[1]
        for r in range(8):
            for c in range(8):
                square = py.Rect(x, y, self.squareSize, self.squareSize)
                if (r + c) % 2 == 0:
                    py.draw.rect(screen, self.lightCol, square)
                else:
                    py.draw.rect(screen, self.darkCol, square)
                piece = self.board[r][c]
                try:
                    pieceImage = images[codes.index(piece)]
                    screen.blit(pieceImage, (x, y))
                except:
                    pass
                x += self.squareSize
            x = 0 + self.position[0]
            y += self.squareSize

    def hoverSquare(self, mousePos):
        x = mousePos[0]
        y = mousePos[1]
        col = (x - self.position[0]) // self.squareSize
        row = (y - self.position[1]) // self.squareSize
        if 0 <= col < 8 and 0 <= row < 8:
            return int(row), int(col)
        return None
                