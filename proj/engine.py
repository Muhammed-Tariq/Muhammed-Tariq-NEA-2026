import gameLogic as gl

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

def mirrorPosition(pieceSquareTable):
    return pieceSquareTable[::-1] # Flips top-to-bottom


# Evaluation calculators


def calculateMaterial(board):
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
    for r in range(8):
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
            eval += score
    return eval

def calculateEvaluation(board):
    return calculateMobility(board) + calculateMaterial(board)