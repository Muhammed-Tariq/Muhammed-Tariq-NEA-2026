import pygame as py

py.display.init()
screen = py.display.set_mode((1920, 1080), 0, 32)
py.display.set_icon(py.image.load("assets/gameIcon.png"))
py.display.set_caption("Mockfish")

def mainMenu():
    """The main menu's game loop, which always runs when this program is executed."""

    bg = py.image.load("assets/bg.png")
    screen.blit(bg, (0, 0))

    playing = True
    while playing:
        py.display.flip()
        for event in py.event.get():
            if event.type == py.QUIT:
                playing = False
                py.quit()

mainMenu()

