# keeps track of game state
import pygame

class Player():
    pass

class Button:
    """Create a button, then blit the surface in the while loop"""
 
    def __init__(self, text,  pos, font, bg="black", feedback=""):
        self.x, self.y = pos
        self.font = pygame.font.SysFont("Sans", font)
        if feedback == "":
            self.feedback = "text"
        else:
            self.feedback = feedback
        self.change_text(text, bg)
 
    def change_text(self, text, bg="black"):
        """Change the text when you click"""
        self.text = self.font.render(text, 1, pygame.Color("White"))
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
 
    def show(self, screen):
        screen.blit(self.surface, (self.x, self.y))

    def is_within_bounds(self, x, y):
        if self.x > x or self.y > y:
            return False
        if self.x + self.size[0] < x or self.y + self.size[1] < y:
            return False
        return True

class Grid():
    pass

class Ruutu():
    pass

class Model():

    def __init__(self):
        self.grid = Grid()
        self.players = []

    def update(event):
        pass

    def lock():
        pass

    def unlock():
        pass

    def read(index):
        pass
