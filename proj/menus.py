import pygame as py
import tkinter as tk
import gameLogic as gl
from tkinter import simpledialog
from button import Buttons


# Constants

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
BOARD_WIDTH = 600
BOARD_HEIGHT = 600

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
BUTTON_IMAGE = py.image.load("assets/buttons/button.png")
OPTIONS_BUTTON_IMAGE = py.image.load("assets/buttons/optionsButton.png")

# Image uploads

pieceCodes = ["bB", "bK", "bN", "bP", "bQ", "bR", "wB", "wK", "wN", "wP", "wQ", "wR"]
pieceImages = [py.transform.scale(py.image.load(f"assets/pieceImages/{code}.png"), (BOARD_WIDTH / 8, BOARD_HEIGHT / 8)) for code in pieceCodes]

# Validation

def pgnValidation(data):
    if data == None or data == "": # If no data is entered, return "None" so nothing appears
        return None
    try:
        move = list(map(str, data.split("\n"))) # Splits the data up by line breaks
        for i in move:
            if i[0:6] == "[White":
                whiteName = i[7:len(i) - 1] # Uses string slicing to obtain the names of each team
            elif i[0:6] == "[Black":
                blackName = i[7:len(i) - 1]

        allMoves = list(map(str, move[len(move) - 1].split("."))) # Splits up by period "." to get each move sequence
        allMoves.remove(allMoves[0]) # First element is always "1"

        for i in range(len(allMoves) - 1): 
            beginningTrim = allMoves[i][1:] # Removes the first character (whitespace) of a string
            currentMove = allMoves[i]
            if i < 8: # Removes 2 or 3 characters from the end depending on what the move is
                endTrim = beginningTrim[:-2]
                allMoves[i] = endTrim
            if i >= 8:
                endTrim = beginningTrim[:-3]
                allMoves[i] = endTrim

        flatMoves = []
        for move in allMoves:
            if "{" in move: 
                move = move[:move.index("{")] # Removes comments
            move = move.strip() # Removes whitespace
            if not move:
                continue
            flatMoves.extend(move.split())

        moves2D = []
        for i in range(0, len(flatMoves) - 1, 2):
            moves2D.append([flatMoves[i], flatMoves[i + 1]]) # Adds properly formatted moves
        return moves2D, whiteName, blackName
    except:
        return False

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

    playButton = Buttons((960, 400), "assets/buttons/button.png", "Start Game", BUTTON_TEXT, "#FFFFFF", "#9C9C9C") # Initialises buttons with the Buttons class
    analysisButton = Buttons((960, 600), "assets/buttons/button.png", "Analysis", BUTTON_TEXT, "#FFFFFF", "#9C9C9C")
    quitButton = Buttons((960, 800), "assets/buttons/button.png", "Quit", BUTTON_TEXT, "#FFFFFF", "#9C9C9C")
    optionsButton = Buttons((1820, 50), "assets/buttons/optionsButton.png", "Options", SMALL_BUTTON_TEXT, "#FFFFFF", "#9C9C9C")

    allButtons = [playButton, analysisButton, quitButton, optionsButton] # Iterated through to shorten code

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
                if analysisButton.hover(py.mouse.get_pos()):
                    analyseGame()
                    playing = False
                    py.display.init()
                if optionsButton.hover(py.mouse.get_pos()):
                    options()
                    playing = False
                    py.display.init()
                if quitButton.hover(py.mouse.get_pos()):
                    playing = False
                

def initialiseGame():
    # The game initialisation's game loop, which runs when playButton / "Start Game" is clicked

    timeSelectList = ["1 min", "2 mins", "5 mins", "10 mins", "15 mins", "20 mins", "30 mins", "60 mins", "90 mins"] # List to select options
    timeCounter = 0 # Iterates list through
    playerSelectList = ["White", "Black", "Random"]
    playerCounter = 0
    
    bg = py.image.load("assets/bg.png")
    screen.blit(bg, (0, 0))

    titleText = HEADER.render("Initialise Game", True, "#FFFFFF") 
    titleRect = titleText.get_rect(center = (960, 160))
    screen.blit(titleText, titleRect)
    timeSelectText = BUTTON_TEXT.render("Time Select", True, "#FFFFFF") 
    timeSelectRect = timeSelectText.get_rect(center = (640, 575))
    screen.blit(timeSelectText, timeSelectRect)
    playerSelectText = BUTTON_TEXT.render("Player Select", True, "#FFFFFF") 
    playerSelectRect = playerSelectText.get_rect(center = (1280, 575))
    screen.blit(playerSelectText, playerSelectRect)

    singleplayerButton = Buttons((640, 400), "assets/buttons/button.png", "Singleplayer", BUTTON_TEXT, "#FFFFFF", "#9C9C9C")
    multiplayerButton = Buttons((1280, 400), "assets/buttons/button.png", "Multiplayer", BUTTON_TEXT, "#FFFFFF", "#9C9C9C")
    timeSelectButton = Buttons((640, 700), "assets/buttons/button.png", "1 min", BUTTON_TEXT, "#FFFFFF", "#9C9C9C")
    playerSelectButton = Buttons((1280, 700), "assets/buttons/button.png", "White", BUTTON_TEXT, "#FFFFFF", "#9C9C9C")
    backButton = Buttons((100, 1030), "assets/buttons/optionsButton.png", "Back", SMALL_BUTTON_TEXT, "#FFFFFF", "#9C9C9C")

    allButtons = [singleplayerButton, multiplayerButton, timeSelectButton, playerSelectButton, backButton]

    playing = True
    while playing:
        py.display.flip()
        for button in allButtons:
            button.hover(py.mouse.get_pos())
            button.draw(screen)
            timeSelectButton.refresh(screen, timeSelectList[timeCounter]) # Refresh to change text
            playerSelectButton.refresh(screen, playerSelectList[playerCounter])
        for event in py.event.get():
            if event.type == py.QUIT:
                playing = False
                py.quit()
            if event.type == py.MOUSEBUTTONDOWN:
                if singleplayerButton.hover(py.mouse.get_pos()):
                    singleplayer(timeSelectList[timeCounter], playerSelectList[playerCounter])
                    playing = False
                    py.display.init()
                if multiplayerButton.hover(py.mouse.get_pos()):
                    multiplayer(timeSelectList[timeCounter], playerSelectList[playerCounter])
                    playing = False
                    py.display.init()
                if timeSelectButton.hover(py.mouse.get_pos()):
                    timeCounter += 1 # Increments counter to get to another option
                    timeCounter = timeCounter % len(timeSelectList) # Modulus to cycle between options
                    timeSelectButton.draw(screen)
                if playerSelectButton.hover(py.mouse.get_pos()):
                    playerCounter += 1
                    playerCounter = playerCounter % len(playerSelectList)
                    playerSelectButton.draw(screen)
                if backButton.hover(py.mouse.get_pos()):
                    mainMenu()
                    playing = False
                    py.display.init()

def analyseGame():
    # The game analysis game loop, which runs when analysisButton / "Analysis" is clicked

    bg = py.image.load("assets/bg.png")
    screen.blit(bg, (0, 0))

    boardTemp = py.image.load("assets/placeholders/analysisplaceholder.png")
    boardRect = boardTemp.get_rect(center = (960, 500))
    screen.blit(boardTemp, boardRect)

    titleText = BUTTON_TEXT.render("Analysis", True, "#FFFFFF") 
    titleRect = titleText.get_rect(center = (960, 100))
    screen.blit(titleText, titleRect)

    errorText = BUTTON_TEXT.render("Error", True, "#FFFFFF") 
    errorRect = errorText.get_rect(center = (960, 1000))

    successText = BUTTON_TEXT.render("Success", True, "#FFFFFF") 
    successRect = successText.get_rect(center = (960, 1000))

    backButton = Buttons((100, 1030), "assets/buttons/optionsButton.png", "Back", SMALL_BUTTON_TEXT, "#FFFFFF", "#9C9C9C")
    analysisButton = Buttons((650, 850), "assets/buttons/optionsButton.png", "Upload", SMALL_BUTTON_TEXT, "#FFFFFF", "#9C9C9C")

    allButtons = [backButton, analysisButton]

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
                if analysisButton.hover(py.mouse.get_pos()):
                    data = tk.simpledialog.askstring("Entry Window", "Enter PGN/FEN data") # Simpledialog to input data
                    result = pgnValidation(data) # Validates data
                    if result == None:
                        pass
                    elif result != False:
                        screen.blit(successText, successRect)
                    else:
                        screen.blit(errorText, errorRect)
                if backButton.hover(py.mouse.get_pos()):
                    mainMenu()
                    playing = False
                    py.display.init()

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
                    colour1 = tk.simpledialog.askstring("Entry Window", "Enter light-square hex code").strip().upper() # Entry window for hex codes, whitespace removed and capitalised
                    colour2 = tk.simpledialog.askstring("Entry Window", "Enter dark-square hex code").strip().upper()
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

def singleplayer(timeSetting, playerSetting):
    # The singleplayer game loop, which runs when singleplayerButton / "Singleplayer" is clicked

    bg = py.image.load("assets/bg.png")
    screen.blit(bg, (0, 0))

    boardTemp = py.image.load("assets/placeholders/gameplaceholder.png")
    boardRect = boardTemp.get_rect(center = (960, 500))
    screen.blit(boardTemp, boardRect)

    game = gl.Board((960-400, 500-300), BOARD_WIDTH, BOARD_HEIGHT, py.Color("#88A4B0"), py.Color("#E2E2E2"))
    clickCounter = 0
    gl.Board.generateLegalMoves(game)

    titleText = BUTTON_TEXT.render("Singleplayer", True, "#FFFFFF") 
    titleRect = titleText.get_rect(center = (960, 100))
    screen.blit(titleText, titleRect)

    resignButton = Buttons((650, 850), "assets/buttons/optionsButton.png", "Resign", SMALL_BUTTON_TEXT, "#FFFFFF", "#9C9C9C")
    drawButton = Buttons((835, 850), "assets/buttons/optionsButton.png", "Draw", SMALL_BUTTON_TEXT, "#FFFFFF", "#9C9C9C")

    allButtons = [resignButton, drawButton]

    playing = True
    while playing:
        gl.Board.drawBoard(game, screen, pieceCodes, pieceImages)
        py.display.flip()
        for button in allButtons:
            button.hover(py.mouse.get_pos())
            button.draw(screen)
        for event in py.event.get():
            if event.type == py.QUIT:
                playing = False
                py.quit()
            if event.type == py.MOUSEBUTTONDOWN:
                pos2 = gl.Board.hoverSquare(game, py.mouse.get_pos())
                if clickCounter == 0:
                    pos1 = pos2
                    clickCounter += 1
                elif clickCounter == 1:
                    if pos1 == pos2:
                        clickCounter = 0
                        pos1 = None
                        pos2 = None
                    else:
                        gl.Board.move(game, pos1, pos2)
                        gl.Board.generateLegalMoves(game)
                        clickCounter = 0
                if resignButton.hover(py.mouse.get_pos()):
                    mainMenu()
                    playing = False
                    py.display.init()
                if drawButton.hover(py.mouse.get_pos()):
                    mainMenu()
                    playing = False
                    py.display.init()

def multiplayer(timeSetting, playerSetting):
    # The options game loop, which runs when multiplayerButton / "Multiplayer" is clicked

    bg = py.image.load("assets/bg.png")
    screen.blit(bg, (0, 0))

    boardTemp = py.image.load("assets/placeholders/gameplaceholder.png")
    boardRect = boardTemp.get_rect(center = (960, 500))
    screen.blit(boardTemp, boardRect)

    titleText = BUTTON_TEXT.render("Multiplayer", True, "#FFFFFF") 
    titleRect = titleText.get_rect(center = (960, 100))
    screen.blit(titleText, titleRect)

    resignButton = Buttons((650, 850), "assets/buttons/optionsButton.png", "Resign", SMALL_BUTTON_TEXT, "#FFFFFF", "#9C9C9C")
    drawButton = Buttons((835, 850), "assets/buttons/optionsButton.png", "Draw", SMALL_BUTTON_TEXT, "#FFFFFF", "#9C9C9C")

    allButtons = [resignButton, drawButton]

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
                if resignButton.hover(py.mouse.get_pos()):
                    mainMenu()
                    playing = False
                    py.display.init()
                if drawButton.hover(py.mouse.get_pos()):
                    mainMenu()
                    playing = False
                    py.display.init()

mainMenu()
py.quit()