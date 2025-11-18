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
                    if (pos1, pos2) in self.legalMoves:
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
        valid = []
        if self.whiteToMove:
            if r != 0:
                if self.board[r - 1][c] == "":
                    valid.append(((r, c), (r - 1, c)))
                if c != 0:  # Diagonal left captures
                    if self.board[r - 1][c - 1] != "":  # Prevents indexing a blank square
                        if self.board[r - 1][c - 1][0] == "b":
                            valid.append(((r, c), (r - 1, c - 1)))
                if c != 7:  # Diagonal right captures
                    if self.board[r - 1][c + 1] != "":
                        if self.board[r - 1][c + 1][0] == "b":
                            valid.append(((r, c), (r - 1, c + 1)))
                if r == 6:
                    if self.board[r - 1][c] == "" and self.board[r - 2][c] == "":
                        valid.append(((r, c), (r - 2, c)))
        else: # Reflected for Black
            if r != 7:
                if self.board[r + 1][c] == "":
                    valid.append(((r, c), (r + 1, c)))
                if c != 0:
                    if self.board[r + 1][c - 1] != "":
                        if self.board[r + 1][c - 1][0] == "w":
                            valid.append(((r, c), (r + 1, c - 1)))
                if c != 7:
                    if self.board[r + 1][c + 1] != "":
                        if self.board[r + 1][c + 1][0] == "w":
                            valid.append(((r, c), (r + 1, c + 1)))
                if r == 1:
                    if self.board[r + 1][c] == "" and self.board[r + 2][c] == "":
                        valid.append(((r, c), (r + 2, c)))
        return valid

    def loopedMoves(self, r, c, directions):
        valid = []
        rStart = r
        cStart = c
        for i in directions:
            while 0 <= r <= 7 and 0 <= c <= 7:
                r = r + i[0]
                c = c + i[1]
                if r > 7 or c > 7:
                    break
                if self.board[r][c] == "":
                    valid.append(((rStart, cStart), (r, c)))
                elif self.board[r][c][0] == "b" and self.whiteToMove:
                    valid.append(((rStart, cStart), (r, c)))
                    r = rStart
                    c = cStart
                    break
                elif self.board[r][c][0] == "w" and not self.whiteToMove:
                    valid.append(((rStart, cStart), (r, c)))
                    r = rStart
                    c = cStart
                    break
                elif self.board[r][c][0] == "w" and self.whiteToMove:
                    r = rStart
                    c = cStart
                    break
                elif self.board[r][c][0] == "b" and not self.whiteToMove:
                    r = rStart
                    c = cStart
                    break
        return valid

    def bishopMoves(self, r, c):
        return self.loopedMoves(r, c, [(-1, -1), (1, -1), (-1, 1), (1, 1)])


    def rookMoves(self, r, c):
        return self.loopedMoves(r, c, [(1, 0), (0, 1), (-1, 0), (0, -1)])

    def knightMoves(self, r, c):
        valid = []
        directions = [(-1, -2), (1, -2), (-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1)]
        for i in directions:
            rNew = r + i[0]
            cNew = c + i[1]
            if 0 <= rNew <= 7 and 0 <= cNew <= 7:
                if self.board[rNew][cNew] == "":
                    valid.append(((r, c), (rNew, cNew)))
                elif self.board[rNew][cNew][0] == "b" and self.whiteToMove:
                    valid.append(((r, c), (rNew, cNew)))
                elif self.board[rNew][cNew][0] == "w" and not self.whiteToMove:
                    valid.append(((r, c), (rNew, cNew)))
        return valid
            

    def queenMoves(self, r, c):
        l1 = self.bishopMoves(r, c)
        l2 = self.rookMoves(r, c)
        return l1 + l2

    def kingMoves(self, r, c):
        valid = []
        directions = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
        for i in directions:
            rNew = r + i[0]
            cNew = c + i[1]
            if 0 <= rNew <= 7 and 0 <= cNew <= 7:
                if self.board[rNew][cNew] == "":
                    valid.append(((r, c), (rNew, cNew)))
                elif self.board[rNew][cNew][0] == "b" and self.whiteToMove:
                    valid.append(((r, c), (rNew, cNew)))
                elif self.board[rNew][cNew][0] == "w" and not self.whiteToMove:
                    valid.append(((r, c), (rNew, cNew)))
        return valid