import pygame as py

# Pygame display initialisation

py.display.init()
py.font.init()
screen = py.display.set_mode((1920, 1080), 0, 32)
py.display.set_icon(py.image.load("assets/gameIcon.png"))
py.display.set_caption("Mockfish")
title = py.font.Font("assets/fonts/RedditSans-Bold.ttf", 32)
buttonText = py.font.Font("assets/fonts/RedditSans-Medium.ttf", 16)

# Helper functions

def writeText(text, font, xy, colour = (255, 255, 255)):
    screen.blit(font.render(text, True, colour), xy)

# Game loops

def mainMenu():
    """The main menu's game loop, which always runs when this program is executed."""

    bg = py.image.load("assets/bg.png")
    screen.blit(bg, (0, 0))

    writeText("Hello", title, (0, 0), (255, 255, 255))

    playing = True
    while playing:
        py.display.flip()
        for event in py.event.get():
            if event.type == py.QUIT:
                playing = False
                py.quit()

mainMenu()