import pygame as py
import engine as en
import math

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
        self.whiteCastle = True # Castling flags
        self.whiteLeftRook = True
        self.whiteRightRook = True
        self.blackCastle = True
        self.blackLeftRook = True
        self.blackRightRook = True
        self.firstMove = True # First move flag
        self.enPassantMoves = [] # Stores the en passant moves that can be made for the next turn
        self.enPassant = 0 # En passant "displacement"
        self.check = False
        self.castlingMoves = [] # Stores the castling moves that can be made for the next turn
        self.previousMove = None # Stores the move just made
        self.pieceImage = None
        self.elapsed = 0 # Time elapsed since piece began moving in smooth movement
        self.animating = False # True if smooth movement is currently ongoing
        self.currentPiece = "" # Piece being moved right now
        self.fiftyMoveCounter = 0 # Stalemate/terminating conditions
        self.repeatCounter = 0
        self.moveCoords = [] # Like moveHistory, but stores coordinates instead

    def drawBoard(self, screen, codes, images, flip = False):
        if self.previousMove is not None: # Ensures we don't index nothing
            ox, oy = self.previousMove[0]
            dx, dy = self.previousMove[1]
        for r in range(8):
            for c in range(8):
                x = 0 + self.position[0] + c * self.squareSize # Computes x and y pixel coordinates based on position of board, square size and column/row number
                y = 0 + self.position[1] + r * self.squareSize
                square = py.Rect(x, y, self.squareSize, self.squareSize)
                if (r + c) % 2 == 0: # Modulus to alternate between light and dark squares
                    py.draw.rect(screen, self.lightCol, square)
                else:
                    py.draw.rect(screen, self.darkCol, square)
                if flip:
                    rF = 7 - r
                    cF = 7 - c
                else:
                    rF = r
                    cF = c
                if self.previousMove is not None: # Previous move highlighting
                    if rF == ox and cF == oy:
                        py.draw.rect(screen, "#ff7b30", square)
                    elif rF == dx and cF == dy:
                        py.draw.rect(screen, "#ffd0b5", square)
                piece = self.board[rF][cF]
                if self.animating and self.previousMove is not None: # Removes piece currently in animation
                    er, ec = self.previousMove[1]
                    if (rF, cF) == (er, ec):
                        piece = ""
                try:
                    pieceImage = images[codes.index(piece)]
                    screen.blit(pieceImage, (x, y)) # Draws piece images
                except:
                    pass

    def smoothPieceMove(self, screen, codes, images, moveTime, flip = False):
        if self.previousMove is None or not self.animating: # If not animating, don't go further
            return
        (r1, c1), (r2, c2) = self.previousMove
        if flip:
            c1 = 7 - c1
            c2 = 7 - c2
            r1 = 7 - r1
            r2 = 7 - r2
        oX = self.position[0] + c1 * self.squareSize
        oY = self.position[1] + r1 * self.squareSize
        dX = self.position[0] + c2 * self.squareSize
        dY = self.position[1] + r2 * self.squareSize
        dt = 1/60
        self.elapsed += dt
        t = self.elapsed / moveTime # Fraction of move that has taken place so far (interpolation)
        if t >= 1.0: # If the whole move has taken place, blit the piece there and stop animating
            pieceImage = images[codes.index(self.pieceImage)]
            screen.blit(pieceImage, (dX, dY))
            self.animating = False
            self.elapsed = 0.0
            return
        p = 0.5 - 0.5 * math.cos(math.pi * t) # Easing function
        x = oX + (dX - oX) * p # Calculates new interpolated position
        y = oY + (dY - oY) * p
        pieceImage = images[codes.index(self.pieceImage)]
        screen.blit(pieceImage, (x, y))

    def generateLegalMoves(self, filterCheck = True):
        self.legalMoves = []
        self.legalMoves.extend(self.enPassantMoves)
        self.enPassantMoves = []
        self.castlingMoves = []
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
                        self.legalMoves.extend(self.castleKing())
                        self.castlingMoves.extend(self.castleKing())
        if filterCheck:
            self.legalMoves = self.filterMoves(self.legalMoves) # Removes moves that place you in check

    def hoverSquare(self, mousePos): # Finds which square the cursor is in
        x = mousePos[0]
        y = mousePos[1]
        col = (x - self.position[0]) // self.squareSize # Integer division to figure out the square the cursor is in
        row = (y - self.position[1]) // self.squareSize
        if 0 <= col < 8 and 0 <= row < 8:
            return int(row), int(col)
        return None

    def move(self, pos1, pos2):
        self.enPassant = 0
        r1, c1 = pos1
        r2, c2 = pos2
        piece1 = self.board[r1][c1]
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
        self.previousMove = (pos1, pos2)
        self.currentPiece = piece1
        self.pieceImage = piece1
        self.elapsed = 0.0
        self.animating = True
        if self.board[r2][c2] != "" or self.enPassant != 0:
            capture = True
        else:
            capture = False
        self.board[r2 + self.enPassant][c2] = piece1
        self.board[r1][c1] = ""
        if self.enPassant != 0:
            self.board[r2][c2] = ""
        self.enPassantCheck(r1, r2, c1, c2, piece1)
        self.promote(piece1, r2, c2)
        self.castleRook(pos1, pos2, piece1)
        self.moveCoords.append((pos1, pos2))
        if len(self.moveCoords) >= 8: # Increments repeat counter if the previous two full moves are the same as the two full moves before that
            if self.moveCoords[-8:-4] == self.moveCoords[-4:]:
                self.repeatCounter += 1
            else:
                self.repeatCounter = 0
        self.whiteToMove = not self.whiteToMove # Change turns (white to black/black to white)
        if self.whiteToMove:
            side = "w" 
        else: 
            side = "b"
        self.check = self.inCheck(side)
        if self.check:
            self.moveHistory[-1] += "+"
        if piece1[1] == "P" or capture: # Increments fifty-move counter if a pawn hasn't moved or if no captures are made
            self.fiftyMoveCounter = 0
        else:
            self.fiftyMoveCounter += 1
        self.firstMove = False # For the timer logic
        return True

    def indextoACN(self, pos1, pos2, piece):
        if piece == "":
            return ""
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
            if piece[1] != "P": # Non-pawn movement
                if self.board[r2][c2] != "":
                    acn = str(piece[1]) + "x" + str(col2) + str(row2) # Captures
                else:
                    acn = str(piece[1]) + str(col2) + str(row2)
            else:
                if self.board[r2][c2] != "": # Pawn movement
                    acn = str(col1) + "x" + str(col2) + str(row2) # Captures
                else:
                    acn = str(col2) + str(row2)
        return acn


    # Piece movements


    def pawnMoves(self, r, c):
        valid = []
        if self.whiteToMove:
            if r != 0: # Prevents indexing out of bounds
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

    def loopedMoves(self, r, c, directions): # Used for almost all piece movements, as all is needed are their directions (seen below)
        valid = []
        rStart = r
        cStart = c
        for i in directions:
            r = rStart # Goes back to the origin square each time a new direction is started
            c = cStart
            while True:
                r = r + i[0] # Adds the direction onto the square before, traversing through it
                c = c + i[1]
                if (r > 7 or c > 7) or not (0 <= r <= 7 and 0 <= c <= 7): # If out of bounds...
                    break
                if self.board[r][c] == "": # If square is blank, you can move to it
                    valid.append(((rStart, cStart), (r, c))) 
                elif self.board[r][c][0] == "b" and self.whiteToMove: # If the square contains a piece of the opposite colour, you can capture it but not go further
                    valid.append(((rStart, cStart), (r, c)))
                    break
                elif self.board[r][c][0] == "w" and not self.whiteToMove:
                    valid.append(((rStart, cStart), (r, c)))
                    break
                elif self.board[r][c][0] == "w" and self.whiteToMove: # If the square contains a piece of the same colour...
                    break
                elif self.board[r][c][0] == "b" and not self.whiteToMove:
                    break
                if self.board[rStart][cStart][1] == "N" or self.board[rStart][cStart][1] == "K": # If the piece being moved is a king or knight...
                    break
        return valid

    def bishopMoves(self, r, c):
        return self.loopedMoves(r, c, [(-1, -1), (1, -1), (-1, 1), (1, 1)])

    def rookMoves(self, r, c):
        return self.loopedMoves(r, c, [(1, 0), (0, 1), (-1, 0), (0, -1)])

    def knightMoves(self, r, c):
        return self.loopedMoves(r, c, [(-1, -2), (1, -2), (-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1)])
            
    def queenMoves(self, r, c):
        return self.bishopMoves(r, c) + self.rookMoves(r, c) # Queen has movement patterns of both the rook and bishop

    def kingMoves(self, r, c):
        return self.loopedMoves(r, c, [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)])
    
    def castleKing(self):
        valid = []
        if self.whiteToMove: # Castling for White
            if self.whiteCastle:
                if self.board[7][5] == "" and self.board[7][6] == "" and self.whiteRightRook: # If the respective rook's castling variable is true and the squares in between are empty, you can castle
                    valid.append(((7, 4), (7, 6)))
                if self.board[7][1] == "" and self.board[7][2] == "" and self.board[7][3] == "" and self.whiteLeftRook:
                    valid.append(((7, 4), (7, 2)))
        else: # Castling for Black
            if self.blackCastle:
                if self.board[0][5] == "" and self.board[0][6] == "" and self.blackRightRook:
                    valid.append(((0, 4), (0, 6)))
                if self.board[0][1] == "" and self.board[0][2] == "" and self.board[0][3] == "" and self.blackLeftRook:
                    valid.append(((0, 4), (0, 2)))
        return valid
    
    def castleRook(self, pos1, pos2, piece1):
        if pos1 == (7, 4) and pos2 == (7, 6) and self.whiteCastle and self.whiteRightRook: # Moves the rook when a castling move is known to have been made
            self.board[7][7] = ""
            self.board[7][5] = "wR"
            self.whiteCastle = False
        elif pos1 == (7, 4) and pos2 == (7, 2) and self.whiteCastle and self.whiteLeftRook:
            self.board[7][0] = ""
            self.board[7][3] = "wR"
            self.whiteCastle = False
        elif pos1 == (0, 4) and pos2 == (0, 6) and self.blackCastle and self.blackRightRook:
            self.board[0][7] = ""
            self.board[0][5] = "bR"
            self.blackCastle = False
        elif pos1 == (0, 4) and pos2 == (0, 2) and self.blackCastle and self.blackRightRook:
            self.board[0][0] = ""
            self.board[0][3] = "bR"
            self.blackCastle = False
        if piece1 == "wK": # If the king has moved, castling can never happen again
            self.whiteCastle = False
        if piece1 == "bK":
            self.blackCastle = False
        if pos1 == (7, 7) or pos2 == (7, 7): # If the rook has moved, castling can never happen on that side anymore
            self.whiteRightRook = False
        if pos1 == (7, 0) or pos2 == (7, 0):
            self.whiteLeftRook = False
        if pos1 == (0, 7) or pos2 == (0, 7):
            self.blackRightRook = False
        if pos1 == (0, 0) or pos2 == (0, 0):
            self.blackLeftRook = False
        if not (self.whiteLeftRook or self.whiteRightRook): # If both rook castling variables are False, that side can never castle again
            self.whiteCastle = False
        if not (self.blackLeftRook or self.blackRightRook):
            self.blackCastle = False

    
    # Helper functions


    def legalTargets(self, start): # Obtains all the destination squares a side can move to
        if start == None:
            return []
        else:
            targets = []
            for move in self.legalMoves:
                if move[0] == start:
                    targets.append(move[1])
            return targets
        
    def drawLegalMoves(self, screen, start, flip = False):
        if start == None:
            return
        sr, sc = start
        mover = self.board[sr][sc]
        moverColour = mover[0]
        targets = self.legalTargets(start)
        if not targets: 
            return
        overlay = py.Surface((self.length, self.height), py.SRCALPHA) # Dimensions for rings, surfaces to blit it on
        defaultR = int(self.squareSize * 0.16)
        capR = int(self.squareSize * 0.22)
        ringDiameter  = int(self.squareSize * 0.04)
        for (r, c) in targets: # Draws a circle on each target square
            if flip:
                rF = 7 - r
                cF = 7 - c
            else:
                rF = r
                cF = c
            cx = int(cF * self.squareSize + self.squareSize / 2) 
            cy = int(rF * self.squareSize + self.squareSize / 2)
            targetPiece = self.board[r][c]
            enPassant = 0
            if mover[1] == "P" and targetPiece == "" and abs(r - sr) == 1 and abs(c - sc) == 1: # En passant handling
                if moverColour == "w":
                    enPassant = -1 
                else: 
                    enPassant = 1
            if (targetPiece != "" and targetPiece[0] != moverColour) or enPassant != 0:
                py.draw.circle(overlay, (*(130, 130, 130), 170), (cx, cy), capR, width = ringDiameter)
            else:
                py.draw.circle(overlay, (*(130, 130, 130), 170), (cx, cy), defaultR)
        screen.blit(overlay, self.position)
    
    def kingPos(self, colour = None): # Obtain's the king's position
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

    def noChangeMove(self, pos1, pos2): # Tests a move without changing board states
        self.enPassant = 0
        r1, c1 = pos1
        r2, c2 = pos2
        piece1 = self.board[r1][c1]
        self.enPassantCheck(r1, r2, c1, c2, piece1)
        if piece1 == "wP" and abs(r2 - r1) == 1 and abs(c2 - c1) == 1 and self.board[r2][c2] == "":
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
        self.promote(piece1, r2, c2)
        self.castleRook(pos1, pos2, piece1)

    def enPassantCheck(self, r1, r2, c1, c2, piece1): # If en passant has happened, append to enPassantMoves for the next turn
        if piece1 == "wP" and r1 == 6 and r2 == 4 and c1 == c2:
            if c2 > 0 and self.board[r2][c2 - 1] == "bP":
                self.enPassantMoves.append(((r2, c2 - 1), (r2 + 1, c2)))
            if c2 < 7 and self.board[r2][c2 + 1] == "bP":
                self.enPassantMoves.append(((r2, c2 + 1), (r2 + 1, c2)))
        elif piece1 == "bP" and r1 == 1 and r2 == 3 and c1 == c2:
            if c2 > 0 and self.board[r2][c2 - 1] == "wP":
                self.enPassantMoves.append(((r2, c2 - 1), (r2 - 1, c2)))
            if c2 < 7 and self.board[r2][c2 + 1] == "wP":
                self.enPassantMoves.append(((r2, c2 + 1), (r2 - 1, c2)))

    def promote(self, piece1, r2, c2):
        if piece1 == "wP" and r2 == 0:
            self.board[r2][c2] = "wQ"
        elif piece1 == "bP" and r2 == 7:
            self.board[r2][c2] = "bQ"

    def filterMoves(self, moves):
        keptMoves = []
        for i in moves:
            start = i[0] # Move unpacking
            end = i[1]
            backupBoard = [] # Backing up the entire state of the game
            for row in self.board:
                backupBoard.append(row[:])
            backupEPMoves = list(self.enPassantMoves)
            backupEP = self.enPassant
            backupLegalMoves = list(self.legalMoves)
            backupTurn = self.whiteToMove
            backupWhiteCastle = self.whiteCastle
            backupWhiteLeftRook = self.whiteLeftRook
            backupWhiteRightRook = self.whiteRightRook
            backupBlackCastle = self.blackCastle
            backupBlackLeftRook = self.blackLeftRook
            backupBlackRightRook = self.blackRightRook
            self.noChangeMove(start, end) # Testing the move
            kingPos = self.kingPos() # King position after test move, as the king may have been moved
            self.whiteToMove = not self.whiteToMove
            opponentMoves = []
            for r in range(8): # Generate list of opponent's moves to see if they attack the king
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
            if self.whiteToMove:
                side = "w"
            else:
                side = "b"
            if not kingAttacked:
                keptMoves.append((start, end))
            self.board = backupBoard
            self.enPassantMoves = backupEPMoves
            self.enPassant = backupEP
            self.legalMoves = backupLegalMoves
            self.whiteToMove = backupTurn
            self.whiteCastle = backupWhiteCastle
            self.whiteLeftRook = backupWhiteLeftRook
            self.whiteRightRook = backupWhiteRightRook
            self.blackCastle = backupBlackCastle
            self.blackLeftRook = backupBlackLeftRook
            self.blackRightRook = backupBlackRightRook
            if (start, end) in self.castlingMoves and (start, end) in keptMoves and self.inCheck(side): # Prevents castling out of check
                keptMoves.remove((start, end))
        return keptMoves

    def inCheck(self, colour): # Determines if a side is currently in check
        kingPos = self.kingPos(colour)
        backupTurn = self.whiteToMove
        if colour == "b":
            self.whiteToMove = True
        else:
            self.whiteToMove = False
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

