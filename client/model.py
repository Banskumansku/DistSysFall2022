# keeps track of game state
import pygame

import copy

from eventmanager import EventManager, ReadBoardEvent, UpdateBoardEvent, BoardStateEvent, ResetBoardEvent

from enum import Enum

class Button:
 
    def __init__(self, text,  pos, font):
        self.x, self.y = pos
        self.font = pygame.font.SysFont("Sans", font)
        self.change_text(text, "white")
 
    def change_text(self, text, bg):

        # Render the text of the button

        self.text = self.font.render(text, 1, pygame.Color("Black"))
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
 
    def show(self, screen):

        # Render the button onto something else

        screen.blit(self.surface, (self.x, self.y))

    def is_within_bounds(self, x, y):

        # Check if click is in bounds

        if self.x > x or self.y > y:
            return False
        if self.x + self.size[0] < x or self.y + self.size[1] < y:
            return False
        return True

# Enum representing a square

class Ruutu(Enum):
    EMPTY = 0
    NOUGHT = 1
    CROSS = 2

# The state of the game

class Model():

    def __init__(self):
        self.reset_state()

    def reset_state(self):

        # A blank grid

        self.grid = []
        self.players = []
        for y in range(3):
            row = []
            for x in range(3):
                row.append(Ruutu.EMPTY)
            self.grid.append(row)

    # Register to the event manager and keep a handle to it

    def set_event_manager(self, event_manager):
        self.event_manager = event_manager
        self.event_manager.RegisterListener(self)

    # List of the end points of the winning rows

    def winning_rows(self):
        result = []

        # Horizontal

        for hline in range(3):
            k = self.grid[hline][0]
            if k == Ruutu.EMPTY:
                continue
            if k == self.grid[hline][1] and k == self.grid[hline][2]:
                result.append([[0, hline], [2, hline]])

        # Vertical

        for vline in range(3):
            k = self.grid[0][vline]
            if k == Ruutu.EMPTY:
                continue
            if k == self.grid[1][vline] and k == self.grid[2][vline]:
                result.append([[vline, 0], [vline, 2]])

        # Diagonal 1

        if self.grid[0][0] != Ruutu.EMPTY and self.grid[0][0] == self.grid[1][1] and self.grid[0][0] == self.grid[2][2]:
            result.append([[0, 0], [2, 2]])

        # Diagonal 2

        if self.grid[2][0] != Ruutu.EMPTY and self.grid[2][0] == self.grid[1][1] and self.grid[2][0] == self.grid[0][2]:
            result.append([[2, 0], [0, 2]])

        return result

    def notify(self, event):
        
        # Inform the world about the board upon request

        if isinstance(event, ReadBoardEvent):
            self.event_manager.Post(BoardStateEvent(copy.deepcopy(self.grid), self.winning_rows()))
        
        # Update the state of the board

        if isinstance(event, UpdateBoardEvent):
            self.grid[event.y][event.x] = event.payload
            self.event_manager.Post(BoardStateEvent(copy.deepcopy(self.grid), self.winning_rows()))

        # Reset the board

        if isinstance(event, ResetBoardEvent):
            self.reset_state()
            self.event_manager.Post(BoardStateEvent(copy.deepcopy(self.grid), self.winning_rows()))
