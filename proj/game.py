import time
import random
import pygame as py
import tkinter as tk
import gameLogic as gl
import engine as en
from tkinter import simpledialog
from button import Buttons

root = tk.Tk()
root.withdraw()

# Constants/variables to initialise

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
BOARD_WIDTH = 600
BOARD_HEIGHT = 600

clock = py.time.Clock()

# Pygame display initialisation

py.display.init()
py.font.init()

screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

py.display.set_icon(py.image.load("assets/gameIcon.png"))
py.display.set_caption("Mockfish")

TITLE = py.font.Font("assets/fonts/RedditSans-Bold.ttf", 150)
HEADER = py.font.Font("assets/fonts/RedditSans-Bold.ttf", 100)
BUTTON_TEXT = py.font.Font("assets/fonts/RedditSans-Bold.ttf", 52)
SMALL_BUTTON_TEXT = py.font.Font("assets/fonts/RedditSans-Bold.ttf", 35)
TIMER_TEXT = py.font.Font("assets/fonts/IBMPlexSans-SemiBold.ttf", 50)
SMALL_TEXT = py.font.Font("assets/fonts/RedditSans-Bold.ttf", 25)
SMALLER_TEXT = py.font.Font("assets/fonts/RedditSans-Medium.ttf", 20)
BUTTON_IMAGE = py.image.load("assets/buttons/button.png")
OPTIONS_BUTTON_IMAGE = py.image.load("assets/buttons/optionsButton.png")

# Image uploads

pieceCodes = ["bB", "bK", "bN", "bP", "bQ", "bR", "wB", "wK", "wN", "wP", "wQ", "wR"]
pieceImages = [py.transform.scale(py.image.load(f"assets/pieceImages/{code}.png"), (BOARD_WIDTH / 8, BOARD_HEIGHT / 8)) for code in pieceCodes]

# Functions and validation

def hexValidation(data):
    if data == None or data == "": # If no data is entered, return "None" so nothing appears
        return None
    if data[0] != "#": # Every hex code must include a hashtag
        return False
    if len(data) != 4 and len(data) != 7: # Every hex code (including the hashtag) is either 4 or 7 characters long
        return False
    for i in range(1, len(data)):
        character = data[i]
        if not (character.isdigit() or character in ["A", "B", "C", "D", "E", "F"]): # All hex codes are either digits or letters A-F
            return False
    return True

# Game loops

def mainMenu():
    # The main menu's game loop, which always runs when this program is executed

    bg = py.image.load("assets/bg.png") # Loads the background
    screen.blit(bg, (0, 0)) # Places the background onto the screen

    titleText = TITLE.render("Mockfish", True, "#FFFFFF") # Renders the text
    titleRect = titleText.get_rect(center = (960, 160)) # Rectangle for alignment
    screen.blit(titleText, titleRect)

    playButton = Buttons((960, 500), "assets/buttons/button.png", "Start Game", BUTTON_TEXT, "#FFFFFF", "#9C9C9C") # Initialises buttons with the Buttons class
    quitButton = Buttons((960, 700), "assets/buttons/button.png", "Quit", BUTTON_TEXT, "#FFFFFF", "#9C9C9C")
    optionsButton = Buttons((1820, 50), "assets/buttons/optionsButton.png", "Options", SMALL_BUTTON_TEXT, "#FFFFFF", "#9C9C9C")

    allButtons = [playButton, quitButton, optionsButton] # Iterated through to shorten code

    playing = True # Game loop; true by default when a menu is opened
    while playing:
        py.display.flip() # Update screen
        for button in allButtons:
            button.hover(py.mouse.get_pos())
            button.draw(screen)
        for event in py.event.get():
            if event.type == py.QUIT: # If the X button is clicked, close the game
                playing = False
                py.quit()
            if event.type == py.MOUSEBUTTONDOWN: # If the mouse button is clicked...
                if playButton.hover(py.mouse.get_pos()): # ...and the mouse is hovering over one of the buttons...
                    initialiseGame() # ...an action occurs
                    playing = False
                    py.display.init()
                if optionsButton.hover(py.mouse.get_pos()):
                    options()
                    playing = False
                    py.display.init()
                if quitButton.hover(py.mouse.get_pos()):
                    playing = False
        clock.tick(60)
                

def initialiseGame():
    # The game initialisation's game loop, which runs when playButton / "Start Game" is clicked

    timeSelectList = ["1 min", "2 mins", "5 mins", "10 mins", "15 mins", "20 mins", "30 mins", "60 mins", "90 mins"] # List to select options
    timeCounter = 0 # Iterates list through
    
    bg = py.image.load("assets/bg.png")
    screen.blit(bg, (0, 0))

    titleText = HEADER.render("Initialise Game", True, "#FFFFFF") 
    titleRect = titleText.get_rect(center = (960, 160))
    screen.blit(titleText, titleRect)
    timeSelectText = BUTTON_TEXT.render("Time Select", True, "#FFFFFF") 
    timeSelectRect = timeSelectText.get_rect(center = (960, 575))
    screen.blit(timeSelectText, timeSelectRect)

    singleplayerButton = Buttons((640, 400), "assets/buttons/button.png", "Singleplayer", BUTTON_TEXT, "#FFFFFF", "#9C9C9C")
    multiplayerButton = Buttons((1280, 400), "assets/buttons/button.png", "Multiplayer", BUTTON_TEXT, "#FFFFFF", "#9C9C9C")
    timeSelectButton = Buttons((960, 700), "assets/buttons/button.png", "1 min", BUTTON_TEXT, "#FFFFFF", "#9C9C9C")
    backButton = Buttons((100, 1030), "assets/buttons/optionsButton.png", "Back", SMALL_BUTTON_TEXT, "#FFFFFF", "#9C9C9C")

    allButtons = [singleplayerButton, multiplayerButton, timeSelectButton, backButton]

    playing = True
    while playing:
        py.display.flip()
        for button in allButtons:
            button.hover(py.mouse.get_pos())
            button.draw(screen)
            timeSelectButton.refresh(screen, timeSelectList[timeCounter]) # Refresh to change text
        for event in py.event.get():
            if event.type == py.QUIT:
                playing = False
                py.quit()
            if event.type == py.MOUSEBUTTONDOWN:
                if singleplayerButton.hover(py.mouse.get_pos()):
                    difficultySelect(timeSelectList[timeCounter])
                    playing = False
                    py.display.init()
                if multiplayerButton.hover(py.mouse.get_pos()):
                    multiplayer(timeSelectList[timeCounter])
                    playing = False
                    py.display.init()
                if timeSelectButton.hover(py.mouse.get_pos()):
                    timeCounter += 1 # Increments counter to get to another option
                    timeCounter = timeCounter % len(timeSelectList) # Modulus to cycle between options
                    timeSelectButton.draw(screen)
                if backButton.hover(py.mouse.get_pos()):
                    mainMenu()
                    playing = False
                    py.display.init()
        clock.tick(60)

def options():
    # The options game loop, which runs when optionsButton / "Options" is clicked

    bg = py.image.load("assets/bg.png")
    screen.blit(bg, (0, 0))

    titleText = HEADER.render("Options", True, "#FFFFFF") 
    titleRect = titleText.get_rect(center = (960, 160))
    screen.blit(titleText, titleRect)

    errorText = BUTTON_TEXT.render("Error", True, "#FFFFFF") 
    errorRect = errorText.get_rect(center = (960, 1000))

    successText = BUTTON_TEXT.render("Success", True, "#FFFFFF") 
    successRect = successText.get_rect(center = (960, 1000))

    colourButton = Buttons((960, 400), "assets/buttons/button.png", "Colours", BUTTON_TEXT, "#FFFFFF", "#9C9C9C")
    backButton = Buttons((100, 1030), "assets/buttons/optionsButton.png", "Back", SMALL_BUTTON_TEXT, "#FFFFFF", "#9C9C9C")

    allButtons = [backButton, colourButton]

    playing = True
    while playing:
        py.display.flip()
        for button in allButtons:
            button.hover(py.mouse.get_pos())
            button.draw(screen)
        for event in py.event.get():
            if event.type == py.QUIT:
                playing = False
                py.quit()
            if event.type == py.MOUSEBUTTONDOWN:
                if colourButton.hover(py.mouse.get_pos()):
                    colour1 = simpledialog.askstring("Entry Window", "Enter light-square hex code").strip().upper() # Entry window for hex codes, whitespace removed and capitalised
                    colour2 = simpledialog.askstring("Entry Window", "Enter dark-square hex code").strip().upper()
                    result1 = hexValidation(colour1)
                    result2 = hexValidation(colour2)
                    if not result1 or not result2:
                        screen.blit(errorText, errorRect)
                    else:
                        screen.blit(successText, successRect)
                if backButton.hover(py.mouse.get_pos()):
                    mainMenu()
                    playing = False
                    py.display.init()
        clock.tick(60)

def difficultySelect(timeSetting):
    # The difficulty selection game loop, which runs when "Start Game" > "Singleplayer" is clicked

    playerSelectList = ["White", "Black", "Random"]
    playerCounter = 0

    bg = py.image.load("assets/bg.png")
    screen.blit(bg, (0, 0))

    titleText = HEADER.render("Singleplayer Game", True, "#FFFFFF")
    titleRect = titleText.get_rect(center = (960, 160))
    screen.blit(titleText, titleRect)
    timeSelectText = BUTTON_TEXT.render("Player Select", True, "#FFFFFF") 
    timeSelectRect = timeSelectText.get_rect(center = (1200, 475))
    screen.blit(timeSelectText, timeSelectRect)

    easyButton = Buttons((760, 400), "assets/buttons/button.png", "Easy", BUTTON_TEXT, "#FFFFFF", "#9C9C9C")
    mediumButton = Buttons((760, 600), "assets/buttons/button.png", "Medium", BUTTON_TEXT, "#FFFFFF", "#9C9C9C")
    hardButton = Buttons((760, 800), "assets/buttons/button.png", "Hard", BUTTON_TEXT, "#FFFFFF", "#9C9C9C")
    playerSelectButton = Buttons((1200, 600), "assets/buttons/button.png", "White", BUTTON_TEXT, "#FFFFFF", "#9C9C9C")
    backButton = Buttons((100, 1030), "assets/buttons/optionsButton.png", "Back", SMALL_BUTTON_TEXT, "#FFFFFF", "#9C9C9C")

    allButtons = [easyButton, mediumButton, hardButton, backButton]

    playing = True
    while playing:
        py.display.flip()
        for button in allButtons:
            button.hover(py.mouse.get_pos())
            button.draw(screen)
            playerSelectButton.refresh(screen, playerSelectList[playerCounter])
        for event in py.event.get():
            if event.type == py.QUIT:
                playing = False
                py.quit()
            if event.type == py.MOUSEBUTTONDOWN:
                if easyButton.hover(py.mouse.get_pos()):
                    singleplayer(timeSetting, playerSelectList[playerCounter], "E")
                    playing = False
                    py.display.init()
                if mediumButton.hover(py.mouse.get_pos()):
                    singleplayer(timeSetting, playerSelectList[playerCounter], "M")
                    playing = False
                    py.display.init()
                if hardButton.hover(py.mouse.get_pos()):
                    singleplayer(timeSetting, playerSelectList[playerCounter], "H")
                    playing = False
                    py.display.init()
                if playerSelectButton.hover(py.mouse.get_pos()):
                    playerCounter += 1
                    playerCounter = playerCounter % len(playerSelectList)
                    playerSelectButton.draw(screen)
                if backButton.hover(py.mouse.get_pos()):
                    mainMenu()
                    playing = False
                    py.display.init()
        clock.tick(60)

def multiplayer(timeSetting):
    # The multiplayer game loop, which runs when multiplayerButton / "Multiplayer" is clicked

    convTime = int(timeSetting[:2].strip())
    whiteMinutes = convTime
    whiteSeconds = 0
    blackMinutes = convTime
    blackSeconds = 0

    interval1 = 0
    timeElapsed = 0
    total = 0

    movePairs = []

    bg = py.image.load("assets/bg.png")
    screen.blit(bg, (0, 0))

    boardTemp = py.image.load("assets/boardImages/boardMenu.png")
    boardRect = boardTemp.get_rect(center = (960, 500))
    screen.blit(boardTemp, boardRect)

    game = gl.Board((960-400, 500-300), BOARD_WIDTH, BOARD_HEIGHT, py.Color("#88A4B0"), py.Color("#E2E2E2"))
    selected = None
    game.generateLegalMoves()
    gl.Board.generateLegalMoves(game)

    titleText = BUTTON_TEXT.render("Multiplayer", True, "#FFFFFF") 
    titleRect = titleText.get_rect(center = (960, 100))
    screen.blit(titleText, titleRect)

    whiteText = SMALL_TEXT.render("White", True, "#FFFFFF")
    whiteRect = whiteText.get_rect(center = (1260, 760))
    screen.blit(whiteText, whiteRect)
    blackText = SMALL_TEXT.render("Black", True, "#FFFFFF")
    blackRect = blackText.get_rect(center = (1260, 235))
    screen.blit(blackText, blackRect)
    if whiteMinutes > 10:
        zero = ""
    else:
        zero = "0"
    whiteTimerText = TIMER_TEXT.render(zero + str(whiteMinutes) + ":" + "00", True, "#FFFFFF")
    whiteTimerRect = whiteTimerText.get_rect(center = (1260, 710))
    screen.blit(whiteTimerText, whiteTimerRect)
    blackTimerText = TIMER_TEXT.render(zero + str(blackMinutes) + ":" + "00", True, "#FFFFFF")
    blackTimerRect = whiteTimerText.get_rect(center = (1260, 285))
    screen.blit(blackTimerText, blackTimerRect)

    backButton = Buttons((100, 1030), "assets/buttons/optionsButton.png", "Back", SMALL_BUTTON_TEXT, "#FFFFFF", "#9C9C9C")

    allButtons = [backButton]

    playing = True
    firstLoop = True
    while playing:
        temp = interval1
        interval1 = time.time()
        if firstLoop:
            timeElapsed = 0
            firstLoop = False
        else:
            timeElapsed = interval1 - temp
        total += timeElapsed
        if total >= 1:
            total = 0
            timeElapsed = 0
            if game.firstMove:
                pass
            else:
                if game.whiteToMove:
                    if whiteSeconds == 0:
                        if whiteMinutes == 0:
                            winner("Black")
                            playing = False
                            py.display.init()
                        whiteMinutes -= 1
                        whiteSeconds = 60
                    whiteSeconds -= 1
                    if whiteMinutes >= 10:
                        zero = ""
                    else:
                        zero = "0"
                    if whiteSeconds >= 10:
                        sZero = ""
                    else:
                        sZero = "0"
                    whiteTimerText = TIMER_TEXT.render(zero + str(whiteMinutes) + ":" + sZero + str(whiteSeconds), True, "#FFFFFF")
                    bgRect = whiteTimerRect.inflate(10, 5)
                    py.draw.rect(screen, "#000000", bgRect)
                    whiteTimerRect = whiteTimerText.get_rect(center = (1260, 710))
                    screen.blit(whiteTimerText, whiteTimerRect)
                if not game.whiteToMove:
                    if blackSeconds == 0:
                        if blackMinutes == 0:
                            winner("White")
                            playing = False
                            py.display.init()
                        blackMinutes -= 1
                        blackSeconds = 60
                    blackSeconds -= 1
                    if blackMinutes >= 10:
                        zero = ""
                    else:
                        zero = "0"
                    if blackSeconds >= 10:
                        sZero = ""
                    else:
                        sZero = "0"
                    blackTimerText = TIMER_TEXT.render(zero + str(blackMinutes) + ":" + sZero + str(blackSeconds), True, "#FFFFFF")
                    blackTimerRect = blackTimerText.get_rect(center = (1260, 285))
                    bgRect = blackTimerRect.inflate(10, 5)
                    py.draw.rect(screen, "#000000", bgRect)
                    screen.blit(blackTimerText, blackTimerRect)
        flip = not game.whiteToMove
        gl.Board.drawBoard(game, screen, pieceCodes, pieceImages, flip = flip)
        gl.Board.drawLegalMoves(game, screen, selected, flip = flip)
        py.display.flip()
        for button in allButtons:
            button.hover(py.mouse.get_pos())
            button.draw(screen)
        for event in py.event.get():
            if event.type == py.QUIT:
                playing = False
                py.quit()
            if event.type == py.MOUSEBUTTONDOWN:
                mousePos = py.mouse.get_pos()
                boardPos = game.hoverSquare(mousePos)
                if backButton.hover(py.mouse.get_pos()):
                    mainMenu()
                    playing = False
                    py.display.init()
                if boardPos != None and flip:
                    r, c = boardPos
                    boardPos = (7 - r, 7 -c)
                if boardPos == None: # Handles off-board clicks
                    selected = None
                    continue
                r, c = boardPos
                piece = game.board[r][c]
                if selected == None:
                    if piece != "" and ((piece[0] == "w" and game.whiteToMove) or (piece[0] == "b" and not game.whiteToMove)):
                        selected = boardPos
                else:
                    if boardPos == selected:
                        selected = None
                    else:
                        if game.move(selected, boardPos):
                            print(game.moveHistory[-1]) # Debugging
                            index = len(game.moveHistory) - 1
                            turn = index // 2 + 1
                            movePairs.append(game.moveHistory[-1])
                            if len(movePairs) == 2:
                                move = str(turn) + ". " + str(movePairs[0]) + " " + str(movePairs[1])
                                movePairs = []
                                moveText = SMALLER_TEXT.render(move, True, "#FFFFFF")
                                moveRect = moveText.get_rect(topleft=(1195, 325 + (15 * ((len(game.moveHistory) - 2) % 22))))
                                if (len(game.moveHistory) - 2) % 22 == 0 and len(game.moveHistory) > 2:
                                    wipeRect = py.Rect(1195, moveRect.top, 150, (650 - moveRect.top))
                                    py.draw.rect(screen, (0, 0, 0), wipeRect)
                                screen.blit(moveText, moveRect)
                            game.generateLegalMoves()
                            if len(game.legalMoves) == 0:
                                if game.whiteToMove:
                                    if game.inCheck("w"):
                                        winner("Black")
                                    else:
                                        winner("Stalemate")
                                else:
                                    if game.inCheck("b"):
                                        winner("White")
                                    else:
                                        winner("Stalemate")
                                playing = False
                                py.display.init()
                                selected = None
                                continue
                            selected = None
                        else:
                            if piece != "" and ((piece[0] == "w" and game.whiteToMove) or (piece[0] == "b" and not game.whiteToMove)):
                                selected = boardPos
        clock.tick(60)

def singleplayer(timeSetting, playerSetting, difficulty):
    # The singleplayer game loop, which runs when singleplayerButton / "Singleplayer" is clicked

    convTime = int(timeSetting[:2].strip())
    whiteMinutes = convTime
    whiteSeconds = 0
    blackMinutes = convTime
    blackSeconds = 0

    interval1 = 0
    timeElapsed = 0
    total = 0

    movePairs = []

    bg = py.image.load("assets/bg.png")
    screen.blit(bg, (0, 0))

    boardTemp = py.image.load("assets/boardImages/boardMenu.png")
    boardRect = boardTemp.get_rect(center = (960, 500))
    screen.blit(boardTemp, boardRect)

    game = gl.Board((960-400, 500-300), BOARD_WIDTH, BOARD_HEIGHT, py.Color("#88A4B0"), py.Color("#E2E2E2"))
    selected = None
    game.generateLegalMoves()
    gl.Board.generateLegalMoves(game)

    if playerSetting == "Random":
        playerSetting = random.choice(["White", "Black"])
    humanWhite = (playerSetting == "White")
    if difficulty == "E":
        depth = 1
    elif difficulty == "M":
        depth = 2
    elif difficulty == "H":
        depth = 3

    titleText = BUTTON_TEXT.render("Singleplayer", True, "#FFFFFF") 
    titleRect = titleText.get_rect(center = (960, 100))
    screen.blit(titleText, titleRect)

    whiteText = SMALL_TEXT.render("White", True, "#FFFFFF")
    whiteRect = whiteText.get_rect(center = (1260, 760))
    screen.blit(whiteText, whiteRect)
    blackText = SMALL_TEXT.render("Black", True, "#FFFFFF")
    blackRect = blackText.get_rect(center = (1260, 235))
    screen.blit(blackText, blackRect)
    if whiteMinutes > 10:
        zero = ""
    else:
        zero = "0"
    whiteTimerText = TIMER_TEXT.render(zero + str(whiteMinutes) + ":" + "00", True, "#FFFFFF")
    whiteTimerRect = whiteTimerText.get_rect(center = (1260, 710))
    screen.blit(whiteTimerText, whiteTimerRect)
    blackTimerText = TIMER_TEXT.render(zero + str(blackMinutes) + ":" + "00", True, "#FFFFFF")
    blackTimerRect = whiteTimerText.get_rect(center = (1260, 285))
    screen.blit(blackTimerText, blackTimerRect)

    resignButton = Buttons((650, 850), "assets/buttons/optionsButton.png", "Resign", SMALL_BUTTON_TEXT, "#FFFFFF", "#9C9C9C")
    drawButton = Buttons((835, 850), "assets/buttons/optionsButton.png", "Draw", SMALL_BUTTON_TEXT, "#FFFFFF", "#9C9C9C")
    backButton = Buttons((100, 1030), "assets/buttons/optionsButton.png", "Back", SMALL_BUTTON_TEXT, "#FFFFFF", "#9C9C9C")

    allButtons = [resignButton, drawButton, backButton]

    playing = True
    firstLoop = True
    while playing:
        temp = interval1
        interval1 = time.time()
        if firstLoop:
            timeElapsed = 0
            firstLoop = False
        else:
            timeElapsed = interval1 - temp
        total += timeElapsed
        if total >= 1:
            total = 0
            timeElapsed = 0
            if game.firstMove:
                pass
            else:
                if game.whiteToMove:
                    if whiteSeconds == 0:
                        if whiteMinutes == 0:
                            winner("Black")
                            playing = False
                            py.display.init()
                        whiteMinutes -= 1
                        whiteSeconds = 60
                    whiteSeconds -= 1
                    if whiteMinutes >= 10:
                        zero = ""
                    else:
                        zero = "0"
                    if whiteSeconds >= 10:
                        sZero = ""
                    else:
                        sZero = "0"
                    whiteTimerText = TIMER_TEXT.render(zero + str(whiteMinutes) + ":" + sZero + str(whiteSeconds), True, "#FFFFFF")
                    bgRect = whiteTimerRect.inflate(10, 5)
                    py.draw.rect(screen, "#000000", bgRect)
                    whiteTimerRect = whiteTimerText.get_rect(center = (1260, 710))
                    screen.blit(whiteTimerText, whiteTimerRect)
                if not game.whiteToMove:
                    if blackSeconds == 0:
                        if blackMinutes == 0:
                            winner("White")
                            playing = False
                            py.display.init()
                        blackMinutes -= 1
                        blackSeconds = 60
                    blackSeconds -= 1
                    if blackMinutes >= 10:
                        zero = ""
                    else:
                        zero = "0"
                    if blackSeconds >= 10:
                        sZero = ""
                    else:
                        sZero = "0"
                    blackTimerText = TIMER_TEXT.render(zero + str(blackMinutes) + ":" + sZero + str(blackSeconds), True, "#FFFFFF")
                    blackTimerRect = blackTimerText.get_rect(center = (1260, 285))
                    bgRect = blackTimerRect.inflate(10, 5)
                    py.draw.rect(screen, "#000000", bgRect)
                    screen.blit(blackTimerText, blackTimerRect)
        gl.Board.drawBoard(game, screen, pieceCodes, pieceImages)
        gl.Board.drawLegalMoves(game, screen, selected)
        py.display.flip()
        if (game.whiteToMove and not humanWhite) or (not game.whiteToMove and humanWhite): # If it's the engine's turn...
            move = en.chooseMove(game, depth)
            if move is None:
                game.generateLegalMoves()  # (safe even though chooseMove already did)
                if len(game.legalMoves) == 0:
                    if game.whiteToMove:
                        if game.inCheck("w"):
                            winner("Black")
                        else:
                            winner("Stalemate")
                    else:
                        if game.inCheck("b"):
                            winner("White")
                        else:
                            winner("Stalemate")
            if game.move(move[0], move[1]):
                print(game.moveHistory[-1]) # Debugging
                index = len(game.moveHistory) - 1
                turn = index // 2 + 1
                movePairs.append(game.moveHistory[-1])
                if len(movePairs) == 2:
                    move = str(turn) + ". " + str(movePairs[0]) + " " + str(movePairs[1])
                    movePairs = []
                    moveText = SMALLER_TEXT.render(move, True, "#FFFFFF")
                    moveRect = moveText.get_rect(topleft=(1195, 325 + (15 * ((len(game.moveHistory) - 2) % 22))))
                    if (len(game.moveHistory) - 2) % 22 == 0 and len(game.moveHistory) > 2:
                        wipeRect = py.Rect(1195, moveRect.top, 150, (650 - moveRect.top))
                        py.draw.rect(screen, (0, 0, 0), wipeRect)
                    screen.blit(moveText, moveRect)
                game.generateLegalMoves()
        for button in allButtons:
            button.hover(py.mouse.get_pos())
            button.draw(screen)
        for event in py.event.get():
            if event.type == py.QUIT:
                playing = False
                py.quit()
            if event.type == py.MOUSEBUTTONDOWN:
                mousePos = py.mouse.get_pos()
                boardPos = game.hoverSquare(mousePos)
                if backButton.hover(py.mouse.get_pos()):
                    mainMenu()
                    playing = False
                    py.display.init()
                if resignButton.hover(py.mouse.get_pos()):
                    if humanWhite:
                        winner("Black")
                    else:
                        winner("White")
                if drawButton.hover(py.mouse.get_pos()):
                    evaluation = en.calculateEvaluation(game.board)
                    if humanWhite:
                        if evaluation >= 0:
                            winner("Stalemate")
                    else:
                        if evaluation <= 0:
                            winner("Stalemate")
                if boardPos == None: # Handles off-board clicks
                    selected = None
                    continue
                r, c = boardPos
                piece = game.board[r][c]
                if selected == None:
                    if piece != "" and ((piece[0] == "w" and game.whiteToMove) or (piece[0] == "b" and not game.whiteToMove)):
                        selected = boardPos
                else:
                    if boardPos == selected:
                        selected = None
                    else:
                        if game.move(selected, boardPos):
                            print(game.moveHistory[-1]) # Debugging
                            index = len(game.moveHistory) - 1
                            turn = index // 2 + 1
                            movePairs.append(game.moveHistory[-1])
                            if len(movePairs) == 2:
                                move = str(turn) + ". " + str(movePairs[0]) + " " + str(movePairs[1])
                                movePairs = []
                                moveText = SMALLER_TEXT.render(move, True, "#FFFFFF")
                                moveRect = moveText.get_rect(topleft=(1195, 325 + (15 * ((len(game.moveHistory) - 2) % 22))))
                                if (len(game.moveHistory) - 2) % 22 == 0 and len(game.moveHistory) > 2:
                                    wipeRect = py.Rect(1195, moveRect.top, 150, (650 - moveRect.top))
                                    py.draw.rect(screen, (0, 0, 0), wipeRect)
                                screen.blit(moveText, moveRect)
                            game.generateLegalMoves()
                            if len(game.legalMoves) == 0:
                                if game.whiteToMove:
                                    if game.inCheck("w"):
                                        winner("Black")
                                    else:
                                        winner("Stalemate")
                                else:
                                    if game.inCheck("b"):
                                        winner("White")
                                    else:
                                        winner("Stalemate")
                                playing = False
                                py.display.init()
                                selected = None
                                continue
                            selected = None
                        else:
                            if piece != "" and ((piece[0] == "w" and game.whiteToMove) or (piece[0] == "b" and not game.whiteToMove)):
                                selected = boardPos
        clock.tick(60)

def winner(result):
    # The end-game loop, which runs when a game ends for any reason
    bg = py.image.load("assets/bg.png")
    screen.blit(bg, (0, 0))
    if result == "White" or result == "Black":
        titleText = HEADER.render(result + " wins!", True, "#FFFFFF")
    else:
        titleText = HEADER.render("Stalemate!", True, "#FFFFFF")
    titleRect = titleText.get_rect(center = (960, 160))
    screen.blit(titleText, titleRect)

    playButton = Buttons((960, 500), "assets/buttons/button.png", "Rematch", BUTTON_TEXT, "#FFFFFF", "#9C9C9C")
    menuButton = Buttons((960, 700), "assets/buttons/button.png", "Menu", BUTTON_TEXT, "#FFFFFF", "#9C9C9C")

    allButtons = [playButton, menuButton]

    playing = True
    while playing:
        py.display.flip()
        for button in allButtons:
            button.hover(py.mouse.get_pos())
            button.draw(screen)
        for event in py.event.get():
            if event.type == py.QUIT:
                playing = False
                py.quit()
            if event.type == py.MOUSEBUTTONDOWN:
                if playButton.hover(py.mouse.get_pos()):
                    initialiseGame()
                    playing = False
                    py.display.init()
                if menuButton.hover(py.mouse.get_pos()):
                    mainMenu()
        clock.tick(60)

mainMenu()
py.quit()