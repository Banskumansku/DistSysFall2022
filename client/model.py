# keeps track of game state
import pygame

import copy

from eventmanager import EventManager, ReadBoardEvent, UpdateBoardEvent, BoardStateEvent

from enum import Enum

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

class Ruutu(Enum):
    EMPTY = 0
    NOUGHT = 1
    CROSS = 2

class Model():

    def __init__(self):
        self.grid = []
        self.players = []
        for y in range(3):
            row = []
            for x in range(3):
                row.append(Ruutu.EMPTY)
            self.grid.append(row)

    def set_event_manager(self, event_manager):
        self.event_manager = event_manager
        self.event_manager.RegisterListener(self)

    def winning_rows(self):
        result = []

        for hline in range(3):
            k = self.grid[hline][0]
            if k == Ruutu.EMPTY:
                continue
            if k == self.grid[hline][1] and k == self.grid[hline][2]:
                result.append([[0, hline], [2, hline]])

        for vline in range(3):
            k = self.grid[0][vline]
            if k == Ruutu.EMPTY:
                continue
            if k == self.grid[1][vline] and k == self.grid[2][vline]:
                result.append([[vline, 0], [vline, 2]])

        if self.grid[0][0] != Ruutu.EMPTY and self.grid[0][0] == self.grid[1][1] and self.grid[0][0] == self.grid[2][2]:
            result.append([[0, 0], [2, 2]])

        if self.grid[2][0] != Ruutu.EMPTY and self.grid[2][0] == self.grid[1][1] and self.grid[2][0] == self.grid[0][2]:
            result.append([[2, 0], [0, 2]])

        return result

    def notify(self, event):
        
        if isinstance(event, ReadBoardEvent):
            self.event_manager.Post(BoardStateEvent(copy.deepcopy(self.grid), self.winning_rows()))
        
        if isinstance(event, UpdateBoardEvent):
            self.grid[event.y][event.x] = event.payload
            self.event_manager.Post(BoardStateEvent(copy.deepcopy(self.grid), self.winning_rows()))
