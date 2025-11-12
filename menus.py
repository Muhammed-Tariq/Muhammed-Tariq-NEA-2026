import pygame as py
from classes import Button

# Constants

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Pygame display initialisation

py.display.init()
py.font.init()

screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

py.display.set_icon(py.image.load("assets/gameIcon.png"))
py.display.set_caption("Mockfish")

TITLE = py.font.Font("assets/fonts/RedditSans-Bold.ttf", 150)
HEADER = py.font.Font("assets/fonts/RedditSans-Bold.ttf", 100)
BUTTON_TEXT = py.font.Font("assets/fonts/RedditSans-Bold.ttf", 55)
SMALL_BUTTON_TEXT = py.font.Font("assets/fonts/RedditSans-Bold.ttf", 35)
BUTTON_IMAGE = py.image.load("assets/buttons/button.png")
OPTIONS_BUTTON_IMAGE = py.image.load("assets/buttons/optionsButton.png")

# Game loops

def mainMenu():
    # The main menu's game loop, which always runs when this program is executed

    bg = py.image.load("assets/bg.png")
    screen.blit(bg, (0, 0))

    titleText = TITLE.render("Mockfish", True, "#FFFFFF") 
    titleRect = titleText.get_rect(center = (960, 160))
    screen.blit(titleText, titleRect)

    playButton = Button((960, 400), "assets/buttons/button.png", "Start Game", BUTTON_TEXT, "#FFFFFF", "#9C9C9C")
    analysisButton = Button((960, 600), "assets/buttons/button.png", "Analysis", BUTTON_TEXT, "#FFFFFF", "#9C9C9C")
    quitButton = Button((960, 800), "assets/buttons/button.png", "Quit", BUTTON_TEXT, "#FFFFFF", "#9C9C9C")
    optionsButton = Button((1820, 50), "assets/buttons/optionsButton.png", "Options", SMALL_BUTTON_TEXT, "#FFFFFF", "#9C9C9C")

    playing = True
    while playing:
        py.display.flip()
        playButton.hover(py.mouse.get_pos())
        playButton.draw(screen)
        analysisButton.hover(py.mouse.get_pos())
        analysisButton.draw(screen)
        quitButton.hover(py.mouse.get_pos())
        quitButton.draw(screen)
        optionsButton.hover(py.mouse.get_pos())
        optionsButton.draw(screen)
        for event in py.event.get():
            if event.type == py.QUIT:
                playing = False
                py.quit()
            if event.type == py.MOUSEBUTTONDOWN: 
                if playButton.hover(py.mouse.get_pos()):
                    initialiseGame()
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

    bg = py.image.load("assets/bg.png")
    screen.blit(bg, (0, 0))

    titleText = HEADER.render("Initialise Game", True, "#FFFFFF") 
    titleRect = titleText.get_rect(center = (960, 160))
    screen.blit(titleText, titleRect)

    backButton = Button((100, 1030), "assets/buttons/optionsButton.png", "Back", SMALL_BUTTON_TEXT, "#FFFFFF", "#9C9C9C")

    playing = True
    while playing:
        backButton.hover(py.mouse.get_pos())
        backButton.draw(screen)
        py.display.flip()
        for event in py.event.get():
            if event.type == py.QUIT:
                playing = False
                py.quit()
            if event.type == py.MOUSEBUTTONDOWN:
                if backButton.hover(py.mouse.get_pos()):
                    mainMenu()
                    playing = False
                    py.display.init()

def analyseGame():
    # The game analysis game loop, which runs when analysisButton / "Analysis" is clicked

    bg = py.image.load("assets/bg.png")
    screen.blit(bg, (0, 0))

    titleText = HEADER.render("Analyse Game", True, "#FFFFFF") 
    titleRect = titleText.get_rect(center = (960, 160))
    screen.blit(titleText, titleRect)

    backButton = Button((100, 1030), "assets/buttons/optionsButton.png", "Back", SMALL_BUTTON_TEXT, "#FFFFFF", "#9C9C9C")

    playing = True
    while playing:
        backButton.hover(py.mouse.get_pos())
        backButton.draw(screen)
        py.display.flip()
        for event in py.event.get():
            if event.type == py.QUIT:
                playing = False
                py.quit()
            if event.type == py.MOUSEBUTTONDOWN:
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

    backButton = Button((100, 1030), "assets/buttons/optionsButton.png", "Back", SMALL_BUTTON_TEXT, "#FFFFFF", "#9C9C9C")

    playing = True
    while playing:
        backButton.hover(py.mouse.get_pos())
        backButton.draw(screen)
        py.display.flip()
        for event in py.event.get():
            if event.type == py.QUIT:
                playing = False
                py.quit()
            if event.type == py.MOUSEBUTTONDOWN:
                if backButton.hover(py.mouse.get_pos()):
                    mainMenu()
                    playing = False
                    py.display.init()

mainMenu()
py.quit()