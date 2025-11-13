import pygame as py

class Button(): 
    def __init__(self, position, filename, text, font, colour, hoverColour): 
        self.image = py.image.load(filename)
        self.position = position
        self.rect = self.image.get_rect(center = position)
        self.height = self.image.get_height()
        self.width = self.image.get_width()
        self.text = text
        self.font = font
        self.colour = colour
        self.hoverColour = hoverColour
        self.tempColour = self.colour

    def draw(self, screen):
        titleText = self.font.render(self.text, True, self.colour) 
        titleRect = titleText.get_rect(center = self.position)
        screen.blit(self.image, self.rect)
        screen.blit(titleText, titleRect)

    def refresh(self, screen, text):
        titleText = self.font.render(text, True, self.colour) 
        titleRect = titleText.get_rect(center = self.position)
        screen.blit(self.image, self.rect)
        screen.blit(titleText, titleRect)

    def hover(self, position):
        if self.rect.collidepoint(position):
            self.colour = self.hoverColour
            return True
        else:
            self.colour = self.tempColour
            return False