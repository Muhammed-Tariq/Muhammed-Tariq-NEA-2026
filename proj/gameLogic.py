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
        self.legalMoves = []
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

    def generateLegalMoves(self):
        self.legalMoves = []
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == "":
                    continue
                if (self.whiteToMove and self.board[r][c][0] == "w") or (not self.whiteToMove and self.board[r][c][0] == "b"):
                    if self.board[r][c][1] == "P":
                        self.legalMoves.extend(self.pawnMoves(r, c))
                    elif self.board[r][c][1] == "R":
                        self.legalMoves.extend(self.rookMoves(r, c))
                    elif self.board[r][c][1] == "N":
                        self.legalMoves.extend(self.knightMoves(r, c))
                    elif self.board[r][c][1] == "B":
                        self.legalMoves.extend(self.bishopMoves(r, c))
                    elif self.board[r][c][1] == "Q":
                        self.legalMoves.extend(self.queenMoves(r, c))
                    elif self.board[r][c][1] == "K":
                        self.legalMoves.extend(self.kingMoves(r, c))
                    


    def hoverSquare(self, mousePos):
        x = mousePos[0]
        y = mousePos[1]
        col = (x - self.position[0]) // self.squareSize
        row = (y - self.position[1]) // self.squareSize
        if 0 <= col < 8 and 0 <= row < 8:
            return int(row), int(col)
        return None
                
    def move(self, pos1, pos2):
        if pos1 != None and pos2 != None:
            r1, c1 = pos1
            r2, c2 = pos2
            piece1 = self.board[r1][c1]
            if piece1 != "":
                if (piece1[0] == "b" and self.whiteToMove == False) or (piece1[0] == "w" and self.whiteToMove == True):
                    if [pos1, pos2] in self.legalMoves:
                        print(self.indextoACN(pos2, piece1))
                        self.moveHistory.append(self.indextoACN(pos2, piece1))
                        self.whiteToMove = not self.whiteToMove
                        self.board[r2][c2] = piece1
                        self.board[r1][c1] = ""

    def indextoACN(self, pos2, piece):
        newPos = [pos2[0] + 1, pos2[1] + 1]
        row = newPos[0]
        col = chr(newPos[1] + 96)
        if piece[1] != "P":
            acn = str(piece[1]) + str(col) + str(row)
        else:
            acn = str(col) + str(row)
        return acn
    
    # Piece movements

    def pawnMoves(self, r, c):
        pass

    def bishopMoves(self, r, c):
        pass

    def knightMoves(self, r, c):
        pass

    def rookMoves(self, r, c):
        pass

    def queenMoves(self, r, c):
        l1 = self.bishopMovements(self, r, c)
        l2 = self.rookMovements(self, r, c)
        return l1 + l2

    def kingMoves(self, r, c):
        pass