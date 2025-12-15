import pygame as py
import time

class Board():
    def __init__(self, position, length, height, darkCol, lightCol):
        self.board = [["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"], 
                      ["bP"] * 8,
                      [""] * 8,
                      [""] * 8,
                      [""] * 8,
                      [""] * 8,
                      ["wP"] * 8,
                      ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]] # Board as a 2D array
        self.moveHistory = [] # Tracks the progress of the game through its historical moves
        self.legalMoves = [] # Stores all legal moves
        self.whiteToMove = True # True if White is to move, False if Black is to move
        self.position = position # User-selected position relative to screen
        self.length = length # Dimensions of board
        self.height = height
        self.squareSize = length / 8 # Board is 8x8
        self.darkCol = darkCol # Dark and light-coloured squares
        self.lightCol = lightCol
        self.whiteCastle = True
        self.whiteLeftRook = True
        self.whiteRightRook = True
        self.blackCastle = True
        self.blackLeftRook = True
        self.blackRightRook = True
        self.firstMove = True

    def drawBoard(self, screen, codes, images):
        x = 0 + self.position[0] # Offset by the position set by the user
        y = 0 + self.position[1]
        for r in range(8):
            for c in range(8):
                square = py.Rect(x, y, self.squareSize, self.squareSize)
                if (r + c) % 2 == 0: # Modulus to alternate between light and dark squares
                    py.draw.rect(screen, self.lightCol, square)
                else:
                    py.draw.rect(screen, self.darkCol, square)
                piece = self.board[r][c]
                try:
                    pieceImage = images[codes.index(piece)]
                    screen.blit(pieceImage, (x, y)) # Draws piece images
                except:
                    pass
                x += self.squareSize # Increments x to move to the next square
            x = 0 + self.position[0]
            y += self.squareSize # Increments y to move to the next row

    def generateLegalMoves(self):
        self.legalMoves = []
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == "": # Prevents indexing a blank string
                    continue
                if (self.whiteToMove and self.board[r][c][0] == "w") or (not self.whiteToMove and self.board[r][c][0] == "b"): # If White and the piece is white, or if Black and the piece is black...
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
                        # self.legalMoves.extend(self.castle(r, c))

    def hoverSquare(self, mousePos):
        x = mousePos[0]
        y = mousePos[1]
        col = (x - self.position[0]) // self.squareSize # Integer division to figure out the square the cursor is in
        row = (y - self.position[1]) // self.squareSize
        if 0 <= col < 8 and 0 <= row < 8:
            return int(row), int(col)
        return None

    def move(self, pos1, pos2):
        if pos1 == None or pos2 == None: # Prevents None from being unpacked
            return False
        r1, c1 = pos1
        r2, c2 = pos2
        piece1 = self.board[r1][c1]
        if piece1 == "": # Prevents an empty string from being indexed
            return False
        if not ((piece1[0] == "w" and self.whiteToMove) or (piece1[0] == "b" and not self.whiteToMove)): # If the piece is black and it's Black's turn, or vice versa...
            return False
        if (pos1, pos2) not in self.legalMoves: # If the movement isn't in the list of legal moves...
            return False
        print(self.indextoACN(pos2, piece1))
        self.moveHistory.append(self.indextoACN(pos2, piece1))
        self.board[r2][c2] = piece1
        self.board[r1][c1] = ""
        if piece1 == "wP" and r2 == 0: # Promotion
            self.board[r2][c2] = "wQ"
        elif piece1 == "bP" and r2 == 7:
            self.board[r2][c2] = "bQ"
        self.whiteToMove = not self.whiteToMove # Change turns (white to black/black to white)
        self.firstMove = False # For the timer logic
        return True

    def indextoACN(self, pos2, piece):
        newPos = [pos2[0] + 1, pos2[1] + 1] # 1-indexes, as is the case in chess
        row = newPos[0]
        col = chr(newPos[1] + 96) # Starts at a, b, c, ... using the chr function
        if piece[1] != "P": # Pawn movements not usually denoted with an extra capital letter
            acn = str(piece[1]) + str(col) + str(row) # String concatenation to form chess movements
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

    def loopedMoves(self, r, c, directions): # Rooks and bishops use the exact same loops to go through their directions
        valid = []
        rStart = r
        cStart = c
        for i in directions:
            r = rStart
            c = cStart
            while 0 <= r <= 7 and 0 <= c <= 7:
                r = r + i[0]
                c = c + i[1]
                if (r > 7 or c > 7) or not (0 <= r <= 7 and 0 <= c <= 7):
                    break
                if self.board[r][c] == "":
                    valid.append(((rStart, cStart), (r, c)))
                elif self.board[r][c][0] == "b" and self.whiteToMove:
                    valid.append(((rStart, cStart), (r, c)))
                    break
                elif self.board[r][c][0] == "w" and not self.whiteToMove:
                    valid.append(((rStart, cStart), (r, c)))
                    break
                elif self.board[r][c][0] == "w" and self.whiteToMove:
                    break
                elif self.board[r][c][0] == "b" and not self.whiteToMove:
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
            if 0 <= rNew <= 7 and 0 <= cNew <= 7: # Prevents IndexErrors
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
        return l1 + l2 # Combines the moves of a rook and bishop

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
    
    def legalTargets(self, start): # Gets the legal moves for a piece
        if start == None: # If nothing selected, there are no targets to highlight
            return []
        else:
            targets = []
            for (s, end) in self.legalMoves: # Iterates through every move in self.legalMoves and appends just the end squares where start matches that square
                if s == start:
                    targets.append(end)
            return targets
    
    def drawLegalMoves(self, screen, start, colour = (130, 130, 130), transparency = 170, defaultRadius = 0.16, captureRadius = 0.22): # Colour is the colour of the circle, transparency is self-explanatory (0-255)
        if start == None: # If nothing is selected, don't draw anything
            return
        sr, sc = start # Unpacks the selected row and selected column
        mover = self.board[sr][sc] # Obtains selected square
        if mover == "": # If selected square is empty, stop
            return
        moverColour = mover[0]  # "w" or "b", uses indexing
        targets = self.legalTargets(start)
        if not targets: # If there are no legal moves, there is nothing to draw
            return
        overlay = py.Surface((self.length, self.height), py.SRCALPHA) # Creates surface the size of the board
        defaultR = int(self.squareSize * defaultRadius) # Computes radii based on square size
        capR   = int(self.squareSize * captureRadius)
        ringDiameter  = max(2, int(self.squareSize * 0.04)) # Thickness of ring
        for (r, c) in targets: # Loop over every legal square
            cx = int(c * self.squareSize + self.squareSize / 2) # Convert board coordinates into pixel coordinates of the center of the square
            cy = int(r * self.squareSize + self.squareSize / 2)
            targetPiece = self.board[r][c] # Obtain what is on the target square
            capture = (targetPiece != "" and targetPiece[0] != moverColour) # True if target square has a piece of a different colour to the current one
            if capture:
                py.draw.circle(overlay, (*colour, transparency), (cx, cy), capR, width = ringDiameter) # Draws a ring around pieces that can be captured
            else:
                py.draw.circle(overlay, (*colour, transparency), (cx, cy), defaultR) # Draws a filled dot for default moves
        screen.blit(overlay, self.position) # Offsets using self.position
    
    # def castle(self, r, c):
    #     valid = []
    #     if self.whiteToMove: # Castling
    #         if self.board[7][0] == "":
    #             self.whiteLeftRook = False
    #         if self.board[7][7] == "":
    #             self.whiteRightRook = False
    #         if self.board[7][4] == "":
    #             self.whiteCastle = False
    #         if piece1 == "wK" and self.whiteCastle:
    #             if self.board[7][5] == "" and self.board[7][6] == "":

