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
BUTTON_TEXT = py.font.Font("assets/fonts/RedditSans-SemiBold.ttf", 55)
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

    playing = True
    while playing:
        py.display.flip()
        playButton.hover(py.mouse.get_pos())
        playButton.draw(screen)
        for event in py.event.get():
            if event.type == py.QUIT:
                playing = False
                py.quit()
            if event.type == py.MOUSEBUTTONDOWN:
                pass

def initialiseGame():
    pass

def analyseGame():
    pass

def options():
    pass



mainMenu()