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
        self.enPassantMoves = []
        self.enPassant = 0
        self.ssLegalMoves = []
        self.check = False

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

    def generateLegalMoves(self, filterCheck = True):
        self.legalMoves = []
        self.legalMoves.extend(self.enPassantMoves)
        self.enPassantMoves = []
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
                        self.legalMoves.extend(self.castle())
        if filterCheck:
            self.legalMoves = self.filterMoves(self.legalMoves)


    def hoverSquare(self, mousePos):
        x = mousePos[0]
        y = mousePos[1]
        col = (x - self.position[0]) // self.squareSize # Integer division to figure out the square the cursor is in
        row = (y - self.position[1]) // self.squareSize
        if 0 <= col < 8 and 0 <= row < 8:
            return int(row), int(col)
        return None

    def move(self, pos1, pos2):
        self.enPassant = 0
        if pos1 == None or pos2 == None: # Prevents None from being unpacked
            return False
        r1, c1 = pos1
        r2, c2 = pos2
        target = self.board[r2][c2]
        if target != "" and target[1] == "K":
            return False
        piece1 = self.board[r1][c1]
        if piece1 == "": # Prevents an empty string from being indexed
            return False
        if not ((piece1[0] == "w" and self.whiteToMove) or (piece1[0] == "b" and not self.whiteToMove)): # If the piece is black and it's Black's turn, or vice versa...
            return False
        if (pos1, pos2) not in self.legalMoves: # If the movement isn't in the list of legal moves...
            return False
        if piece1 == "wP" and abs(r2 - r1) == 1 and abs(c2 - c1) == 1 and self.board[r2][c2] == "": # En passant captures
            self.enPassant = -1
            r2 += 1
            pos2 = (r2, c2)
        if piece1 == "bP" and abs(r2 - r1) == 1 and abs(c2 - c1) == 1 and self.board[r2][c2] == "":
            self.enPassant = 1
            r2 -= 1
            pos2 = (r2, c2)
        self.moveHistory.append(self.indextoACN(pos1, pos2, piece1))
        self.board[r2 + self.enPassant][c2] = piece1
        self.board[r1][c1] = ""
        if self.enPassant != 0:
            self.board[r2][c2] = ""
        if piece1 == "wP" and abs(r2 - r1) == 2: # En passant (for next move)
            if c2 > 0 and self.board[r2][c2 - 1] == "bP":
                self.enPassantMoves.append(((r2, c2 - 1), (r2 + 1, c2)))
            if c2 < 7 and self.board[r2][c2 + 1] == "bP":
                self.enPassantMoves.append(((r2, c2 + 1), (r2 + 1, c2)))
        if piece1 == "bP" and abs(r2 - r1) == 2:
            if c2 > 0 and self.board[r2][c2 - 1] == "wP":
                self.enPassantMoves.append(((r2, c2 - 1), (r2 - 1, c2)))
            if c2 < 7 and self.board[r2][c2 + 1] == "wP":
                self.enPassantMoves.append(((r2, c2 + 1), (r2 - 1, c2)))
        if piece1 == "wP" and r2 == 0: # Promotion
            self.board[r2][c2] = "wQ"
        elif piece1 == "bP" and r2 == 7:
            self.board[r2][c2] = "bQ"
        if pos1 == (7, 4) and pos2 == (7, 6): # Castling
            self.board[7][7] = ""
            self.board[7][5] = "wR"
        elif pos1 == (7, 4) and pos2 == (7, 2):
            self.board[7][0] = ""
            self.board[7][3] = "wR"
        elif pos1 == (0, 4) and pos2 == (0, 6):
            self.board[0][7] = ""
            self.board[0][5] = "bR"
        elif pos1 == (0, 4) and pos2 == (0, 2):
            self.board[0][0] = ""
            self.board[0][3] = "bR"
        self.whiteToMove = not self.whiteToMove # Change turns (white to black/black to white)
        if self.whiteToMove:
            side = "w" 
        else: 
            side = "b"
        self.check = self.inCheck(side)
        if self.check:
            self.moveHistory[-1] += "+"
        self.firstMove = False # For the timer logic
        return True

    def indextoACN(self, pos1, pos2, piece):
        if piece == "":
            return ""
        r1, c1, = pos1
        r2, c2 = pos2
        if (pos1 == (7, 4) and pos2 == (7, 6)) or (pos1 == (0, 4) and pos2 == (0, 6)): # Castling notation
            acn = "O-O"
        elif (pos1 == (7, 4) and pos2 == (7, 2)) or (pos1 == (0, 4) and pos2 == (0, 2)):
            acn = "O-O-O"
        else:
            newPos1 = [pos1[0] + 1, pos1[1] + 1]
            newPos2 = [pos2[0] + 1, pos2[1] + 1] # 1-indexes, as is the case in chess
            row1 = 9 - newPos1[0]
            col1 = chr(newPos1[1] + 96)
            row2 = 9 - newPos2[0]
            col2 = chr(newPos2[1] + 96) # Starts at a, b, c, ... using the chr function
            if piece[1] != "P":
                if self.board[r2][c2] != "":
                    acn = str(piece[1]) + "x" + str(col2) + str(row2)
                else:
                    acn = str(piece[1]) + str(col2) + str(row2)
            else:
                if self.board[r2][c2] != "":
                    acn = str(col1) + "x" + str(col2) + str(row2)
                else:
                    acn = str(col2) + str(row2)
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
    
    def castle(self):
        valid = []
        if self.whiteToMove: # Castling for White
            if self.board[7][0] == "":
                self.whiteLeftRook = False
            if self.board[7][7] == "":
                self.whiteRightRook = False
            if self.board[7][4] == "":
                self.whiteCastle = False
            if self.whiteCastle:
                if self.board[7][5] == "" and self.board[7][6] == "" and self.whiteRightRook:
                    valid.append(((7, 4), (7, 6)))
                if self.board[7][1] == "" and self.board[7][2] == "" and self.board[7][3] == "" and self.whiteLeftRook:
                    valid.append(((7, 4), (7, 2)))
        else: # Castling for Black
            if self.board[0][0] == "":
                self.blackLeftRook = False
            if self.board[0][7] == "":
                self.blackRightRook = False
            if self.board[0][4] == "":
                self.blackCastle = False
            if self.blackCastle:
                if self.board[0][5] == "" and self.board[0][6] == "" and self.blackRightRook:
                    valid.append(((0, 4), (0, 6)))
                if self.board[0][1] == "" and self.board[0][2] == "" and self.board[0][3] == "" and self.blackLeftRook:
                    valid.append(((0, 4), (0, 2)))
        return valid
    
    # Helper functions

    def legalTargets(self, start): # Gets the legal moves for a piece
        if start == None: # If nothing selected, there are no targets to highlight
            return []
        else:
            targets = []
            for move in self.legalMoves: # Iterates through every move in self.legalMoves and appends just the end squares where start matches that square
                if move[0] == start:
                    targets.append(move[1])
            return targets
        
    def drawLegalMoves(self, screen, start, colour = (130, 130, 130), transparency = 170, defaultRadius = 0.16, captureRadius = 0.22): # Colour is the colour of the circle, transparency is self-explanatory (0-255)
        if start == None: # If nothing is selected, don't draw anything
            return
        sr, sc = start # Unpacks the selected row and selected column
        mover = self.board[sr][sc] # Obtains selected square
        moverColour = mover[0]  # "w" or "b", uses indexing
        targets = self.legalTargets(start)
        if not targets: # If there are no legal moves, there is nothing to draw
            return
        overlay = py.Surface((self.length, self.height), py.SRCALPHA) # Creates surface the size of the board
        defaultR = int(self.squareSize * defaultRadius) # Computes radii based on square size
        capR = int(self.squareSize * captureRadius)
        ringDiameter  = int(self.squareSize * 0.04) # Thickness of ring
        for (r, c) in targets: # Loop over every legal square
            cx = int(c * self.squareSize + self.squareSize / 2) # Convert board coordinates into pixel coordinates of the center of the square
            cy = int(r * self.squareSize + self.squareSize / 2)
            targetPiece = self.board[r][c] # Obtain what is on the target square
            enPassant = 0
            if mover[1] == "P" and targetPiece == "" and abs(r - sr) == 1 and abs(c - sc) == 1:
                if moverColour == "w":
                    enPassant = -1 
                else: 
                    enPassant = 1
            if (targetPiece != "" and targetPiece[0] != moverColour) or enPassant != 0:
                py.draw.circle(overlay, (*colour, transparency), (cx, cy), capR, width=ringDiameter)
            else:
                py.draw.circle(overlay, (*colour, transparency), (cx, cy), defaultR)
        screen.blit(overlay, self.position) # Offsets using self.position
    
    def kingPos(self, colour = None):
        if colour == None:
            if self.whiteToMove: 
                colour = "w" 
            else: 
                colour = "b"
        target = colour + "K"
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == target:
                    return (r, c)
        return None

    def noChangeMove(self, pos1, pos2):
        self.enPassant = 0
        r1, c1 = pos1
        r2, c2 = pos2
        piece1 = self.board[r1][c1]
        if piece1 == "wP" and abs(r2 - r1) == 1 and abs(c2 - c1) == 1 and self.board[r2][c2] == "": # En passant captures
            self.enPassant = -1
            r2 += 1
            pos2 = (r2, c2)
        if piece1 == "bP" and abs(r2 - r1) == 1 and abs(c2 - c1) == 1 and self.board[r2][c2] == "":
            self.enPassant = 1
            r2 -= 1
            pos2 = (r2, c2)
        self.board[r2 + self.enPassant][c2] = piece1
        self.board[r1][c1] = ""
        if self.enPassant != 0:
            self.board[r2][c2] = ""
        if piece1 == "wP" and r2 == 0: # Promotion
            self.board[r2][c2] = "wQ"
        elif piece1 == "bP" and r2 == 7:
            self.board[r2][c2] = "bQ"
        if pos1 == (7, 4) and pos2 == (7, 6): # Castling
            self.board[7][7] = ""
            self.board[7][5] = "wR"
        elif pos1 == (7, 4) and pos2 == (7, 2):
            self.board[7][0] = ""
            self.board[7][3] = "wR"
        elif pos1 == (0, 4) and pos2 == (0, 6):
            self.board[0][7] = ""
            self.board[0][5] = "bR"
        elif pos1 == (0, 4) and pos2 == (0, 2):
            self.board[0][0] = ""
            self.board[0][3] = "bR"

    def filterMoves(self, moves):
        keptMoves = []
        for i in moves:
            start = i[0] # Move unpacking
            end = i[1]
            backupBoard = [] # Backing up all moves
            for row in self.board:
                backupBoard.append(row[:])
            backupEPMoves = list(self.enPassantMoves)
            backupEP = self.enPassant
            backupLegalMoves = list(self.legalMoves)
            backupTurn = self.whiteToMove  # Always restore the turn being made
            self.noChangeMove(start, end) # Testing the move
            kingPos = self.kingPos() # King position after test move, as the king may have been moved
            self.whiteToMove = not self.whiteToMove
            opponentMoves = []
            for r in range(8):
                for c in range(8):
                    if self.board[r][c] == "":
                        continue
                    if (self.whiteToMove and self.board[r][c][0] == "w") or (not self.whiteToMove and self.board[r][c][0] == "b"):
                        p = self.board[r][c][1]
                        if p == "P":
                            opponentMoves.extend(self.pawnMoves(r, c))
                        elif p == "R":
                            opponentMoves.extend(self.rookMoves(r, c))
                        elif p == "N":
                            opponentMoves.extend(self.knightMoves(r, c))
                        elif p == "B":
                            opponentMoves.extend(self.bishopMoves(r, c))
                        elif p == "Q":
                            opponentMoves.extend(self.queenMoves(r, c))
                        elif p == "K":
                            opponentMoves.extend(self.kingMoves(r, c))
            self.whiteToMove = not self.whiteToMove
            kingAttacked = False
            for m in opponentMoves: # Check if any of the opponent's moves lead to the king being attacked
                if m[1] == kingPos:
                    kingAttacked = True
                    break
            if not kingAttacked:
                keptMoves.append((start, end))
            self.board = backupBoard
            self.enPassantMoves = backupEPMoves
            self.enPassant = backupEP
            self.legalMoves = backupLegalMoves
            self.whiteToMove = backupTurn
        return keptMoves

    def inCheck(self, colour):
        kingPos = self.kingPos(colour)
        if kingPos is None:
            return False
        backupTurn = self.whiteToMove
        self.whiteToMove = (colour == "b")  # If checking black king, attackers are white (True)
        opponentMoves = []
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == "":
                    continue
                if (self.whiteToMove and self.board[r][c][0] == "w") or (not self.whiteToMove and self.board[r][c][0] == "b"):
                    p = self.board[r][c][1]
                    if p == "P":
                        opponentMoves.extend(self.pawnMoves(r, c))
                    elif p == "R":
                        opponentMoves.extend(self.rookMoves(r, c))
                    elif p == "N":
                        opponentMoves.extend(self.knightMoves(r, c))
                    elif p == "B":
                        opponentMoves.extend(self.bishopMoves(r, c))
                    elif p == "Q":
                        opponentMoves.extend(self.queenMoves(r, c))
                    elif p == "K":
                        opponentMoves.extend(self.kingMoves(r, c))
        self.whiteToMove = backupTurn
        for m in opponentMoves:
            if m[1] == kingPos:
                return True
        return False

