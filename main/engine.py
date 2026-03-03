import gameLogic as gl
import math

# Piece-square tables

pawnMobilityW = [[0, 0, 0, 0, 0, 0, 0, 0],
                [50, 50, 50, 50, 50, 50, 50, 50],
                [10, 10, 20, 30, 30, 20, 10, 10],
                [5, 5, 10, 25, 25, 10, 5, 5],
                [0, 0, 0, 20, 20, 0, 0, 0],
                [5, -5, -10, 0, 0, -10, -5, 5],
                [5, 10, 10, -20, -20, 10, 10, 5],
                [0, 0, 0, 0, 0, 0, 0, 0]]

pawnMobilityB = pawnMobilityW[::-1]

knightMobilityW = [[-50, -40, -30, -30, -30, -30, -40, -50],
                  [-40, -20, 0, 0, 0, 0, -20, -40],
                  [-30, 0, 10, 15, 15, 10, 0, -30],
                  [-30, 5, 15, 20, 20, 15, 5, -30],
                  [-30, 0, 15, 20, 20, 15, 0, -30],
                  [-30, 5, 10, 15, 15, 10, 5, -30],
                  [-40, -20, 0, 5, 5, 0, -20, -40],
                  [-50, -40, -30, -30, -30, -30, -40, -50]]

knightMobilityB = knightMobilityW[::-1]

bishopMobilityW = [[-20, -10, -10, -10, -10, -10, -10, -20],
                  [-10, 0, 0, 0, 0, 0, 0, -10],
                  [-10, 0, 5, 10, 10, 5, 0, -10],
                  [-10, 5, 5, 10, 10, 5, 5, -10],
                  [-10, 0, 10, 10, 10, 10, 0, -10],
                  [-10, 10, 10, 10, 10, 10, 10, -10],
                  [-10, 5, 0, 0, 0, 0, 5, -10],
                  [-20, -10, -10, -10, -10, -10, -10, -20]]

bishopMobilityB = bishopMobilityW[::-1]

rookMobilityW = [[0, 0, 0, 0, 0, 0, 0, 0],
                [5, 10, 10, 10, 10, 10, 10, 5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [0, 0, 0, 5, 5, 0, 0, 0]]

rookMobilityB = rookMobilityW[::-1]

queenMobilityW = [[-20, -10, -10, -5, -5, -10, -10, -20],
                 [-10, 0, 0, 0, 0, 0, 0, -10],
                 [-10, 0, 5, 5, 5, 5, 0, -10],
                 [-5, 0, 5, 5, 5, 5, 0, -5],
                 [0, 0, 5, 5, 5, 5, 0, -5],
                 [-10, 5, 5, 5, 5, 5, 0, -10],
                 [-10, 0, 5, 0, 0, 0, 0, -10],
                 [-20, -10, -10, -5, -5, -10, -10, -20]]

queenMobilityB = queenMobilityW[::-1]

kingMobilityW = [[-30, -40, -40, -50, -50, -40, -40, -30],
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-20, -30, -30, -40, -40, -30, -30, -20],
                [-10, -20, -20, -20, -20, -20, -20, -10],
                [20, 20, 0, 0, 0, 0, 20, 20],   
                [20, 30, 10, 0, 0, 10, 30, 20]]

kingMobilityB = kingMobilityW[::-1]


# Evaluation calculators


def calculateMaterial(board): # Iterates through board and sums the material values of all pieces; Black pieces are negative values, White pieces are positive values
    eval = 0
    for r in range(8):
        for c in range(8):
            if board[r][c] == "":
                 continue
            if board[r][c][0] == "w":
                sign = 1
            else:
                sign = -1
            if board[r][c][1] == "P":
                    eval += 1 * sign
            elif board[r][c][1] in ["N", "B"]:
                    eval += 3 * sign
            elif board[r][c][1] == "R":
                    eval += 5 * sign
            elif board[r][c][1] == "Q":
                    eval += 9 * sign
    return eval
                
def calculateMobility(board):
    eval = 0
    for r in range(8): # Iterates through board and sums the positional values of all pieces based on the piece-square table
        for c in range(8):
            if board[r][c] == "":
                 continue
            if board[r][c][0] == "w":
                if board[r][c][1] == "P":
                    score = pawnMobilityW[r][c] / 100
                elif board[r][c][1] == "N":
                    score = knightMobilityW[r][c] / 100
                elif board[r][c][1] == "B":
                    score = bishopMobilityW[r][c] / 100
                elif board[r][c][1] == "R":
                    score = rookMobilityW[r][c] / 100
                elif board[r][c][1] == "Q":
                    score = queenMobilityW[r][c] / 100
                elif board[r][c][1] == "K":
                    score = kingMobilityW[r][c] / 100
                eval += score
            else:
                if board[r][c][1] == "P":
                    score = pawnMobilityB[r][c] / 100
                elif board[r][c][1] == "N":
                    score = knightMobilityB[r][c] / 100
                elif board[r][c][1] == "B":
                    score = bishopMobilityB[r][c] / 100
                elif board[r][c][1] == "R":
                    score = rookMobilityB[r][c] / 100
                elif board[r][c][1] == "Q":
                    score = queenMobilityB[r][c] / 100
                elif board[r][c][1] == "K":
                    score = kingMobilityB[r][c] / 100
                eval -= score
    return eval

def calculateEvaluation(board): # Total evaluation
    return calculateMobility(board) + calculateMaterial(board) 


# Save/restore game


def saveState(game):
    board = []
    for row in game.board:
        board.append(row[:])
    return (board, game.whiteToMove, list(game.enPassantMoves), game.enPassant, game.whiteCastle, game.whiteLeftRook, game.whiteRightRook, game.blackCastle, game.blackLeftRook, game.blackRightRook, game.firstMove, game.check, list(game.legalMoves))
     
def restoreState(game, state):
    (board, whiteToMove, enPassantMoves, enPassant, whiteCastle, whiteLeftRook, whiteRightRook, blackCastle, blackLeftRook, blackRightRook, firstMove, check, legalMoves) = state
    boardCopy = []
    for row in board:
        boardCopy.append(row[:])
    game.board = boardCopy
    game.whiteToMove = whiteToMove
    game.enPassantMoves = list(enPassantMoves)
    game.enPassant = enPassant
    game.whiteCastle = whiteCastle
    game.whiteLeftRook = whiteLeftRook
    game.whiteRightRook = whiteRightRook
    game.blackCastle = blackCastle
    game.blackLeftRook = blackLeftRook
    game.blackRightRook = blackRightRook
    game.firstMove = firstMove
    game.check = check
    game.legalMoves = list(legalMoves)


# Minimax and alpha-beta


def alphaBeta(game, depth, alpha, beta):
    if depth <= 0:
        return calculateEvaluation(game.board)
    game.generateLegalMoves()
    moves = game.legalMoves
    if len(moves) == 0:
        if game.whiteToMove:
            side = "w"
        else: 
            side = "b"
        if game.inCheck(side):
            if game.whiteToMove:
                return -10000 # Black checkmate
            else: 
                return 10000  # White checkmate
        return 0  # Stalemate
    if game.whiteToMove:
        value = -math.inf
        for move in moves:
                state = saveState(game) # Saves the current state
                start, end = move
                game.noChangeMove(start, end)
                game.whiteToMove = not game.whiteToMove
                value = max(value, alphaBeta(game, depth - 1, alpha, beta))
                restoreState(game, state) # Restores the current state
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
        return value
    else:
        value = math.inf
        for move in moves:
                state = saveState(game)
                start, end = move
                game.noChangeMove(start, end)
                game.whiteToMove = not game.whiteToMove
                value = min(value, alphaBeta(game, depth - 1, alpha, beta))
                restoreState(game, state)
                beta = min(beta, value)
                if alpha >= beta:
                    break
        return value
    
def chooseMove(game, depth):
    game.generateLegalMoves()
    moves = game.legalMoves
    if len(moves) == 0:
        return None
    bestMove = None
    if game.whiteToMove:
        bestValue = -math.inf
        for move in moves: # Iterates through each legal move, and only obtains the move that leads to the best evaluation
            state = saveState(game)
            start, end = move
            game.noChangeMove(start, end)
            game.whiteToMove = not game.whiteToMove
            value = alphaBeta(game, depth - 1, -math.inf, math.inf) # Obtains value of the best position that can be obtained from that move
            restoreState(game, state)
            if value > bestValue: # Only considers the move that maximises the value for Whitte
                bestValue = value
                bestMove = move
    else: # Minimises for Black; symmetric logic
        bestValue = math.inf
        for move in moves:
            state = saveState(game)
            start, end = move
            game.noChangeMove(start, end)
            game.whiteToMove = not game.whiteToMove
            value = alphaBeta(game, depth - 1, -math.inf, math.inf)
            restoreState(game, state)
            if value < bestValue:
                bestValue = value
                bestMove = move
    return bestMove
