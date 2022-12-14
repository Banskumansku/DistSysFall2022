import pygame
import model
from eventmanager import EventManager, ChangeViewEvent, RequestQueueEvent, BoardStateEvent, UpdateBoardEvent, BoardClickedEvent
from broadcast import Broadcaster
import time

# draws different game views (start view, wait view, game view, game over view)


class MainView():

    def __init__(self):
        self.button1 = model.Button(
            "Start a new game",
            (100, 100),
            16)

    def draw(self, screen, board, winning_rows):
        screen.fill((0, 0, 0))  # Fill the screen with black.

        # Redraw screen here
        self.button1.show(screen)

        # Flip the display so that the things we drew actually show up.
        pygame.display.flip()
        pygame.display.set_caption('Welcome to the game')
        pass

    def handle_event(self, event, board):
        if event.type == 1026 and self.button1.is_within_bounds(event.pos[0], event.pos[1]):
            return [RequestQueueEvent()]


class WaitView():
    def draw(self, screen, board, winning_rows):
        screen.fill((255, 0, 0))  # Fill the screen with red.

        # Redraw screen here.

        # Flip the display so that the things we drew actually show up.
        pygame.display.flip()
        pygame.display.set_caption('Waiting for your opponent')
        # draw your animation
        pass

    def handle_event(self, event, board):
        pass


class GameView():
    def draw(self, screen, board, winning_rows):
        screen.fill((0, 0, 0))  # Fill the screen with green.

        # Redraw screen here.

        for hline in range(1, 3):
            pygame.draw.line(screen, (255, 255, 255), (10 + hline*100, 10), (10+hline*100, 310))

        for vline in range(1, 3):
            pygame.draw.line(screen, (255, 255, 255), (10, 10 + vline*100), (310, 10 + vline*100))

        for y in range(3):
            for x in range(3):
                if board[y][x] == model.Ruutu.EMPTY:
                    pygame.draw.line(screen, (255, 255, 255), (10 + 100*x+30, 60+100*y), (10 + 100*x+70, 60+100*y))
                if board[y][x] == model.Ruutu.NOUGHT:
                    pygame.draw.circle(screen, (0, 255, 255), (10 + 100*x+50, 10+100*y+50), 30, 1)
                if board[y][x] == model.Ruutu.CROSS:
                    pygame.draw.line(screen, (255, 0, 255), (10 + 100*x+20, 10+100*y+20), (10 + 100*x+80, 10+100*y+80))
                    pygame.draw.line(screen, (255, 0, 255), (10 + 100*x+20, 10+100*y+80), (10 + 100*x+80, 10+100*y+20))

        for a, b in winning_rows:
            pygame.draw.line(screen, (255, 255, 255), (10 + 100*a[0]+50, 10 + 100*a[1]+50), (10 + 100*b[0]+50, 10 + 100*b[1]+50))

        # Flip the display so that the things we drew actually show up.
        pygame.display.flip()
        pygame.display.set_caption('Game view')

        # draw your animation
        pass

    def handle_event(self, event, board):
        if event.type == 1026:
            x = (event.pos[0] - 10) // 100
            y = (event.pos[1] - 10) // 100
            if x in range(3) and y in range(3):
                return [BoardClickedEvent(x, y)]
            return []

class GameEndView():
    def draw(screen, board, winning_rows):
        screen.fill((0, 0, 255))  # Fill the screen with blue.

        # Redraw screen here.

        # Flip the display so that the things we drew actually show up.
        pygame.display.flip()
        pygame.display.set_caption('Game over')
        pass

    def handle_event(self, event, board):
        pass

class ViewManager():

    def __init__(self):
        self.views = {'Main': None,
                      'Wait': None,
                      'Game': None,
                      'GameEnd': None}
        self.board = None
        self.winning_rows = []
        self.view = "Main"

    def init_views(self):
        self.views = {'Main': MainView(),
                      'Wait': WaitView(),
                      'Game': GameView(),
                      'GameEnd': GameEndView()}

    def set_event_manager(self, event_manager):
        self.event_manager = event_manager
        self.event_manager.RegisterListener(self)

    def notify(self, event):
        if isinstance(event, ChangeViewEvent):
            self.view = event.view

        # Always accept board state events

        if isinstance(event, BoardStateEvent):
            self.board = event.payload
            self.winning_rows = event.winning_rows

    def main_game(self):

        clock = pygame.time.Clock()

        fps = 60.0
        fpsClock = pygame.time.Clock()

        width, height = 640, 480
        screen = pygame.display.set_mode((width, height))

        pygame.init()

        self.init_views()

        dt = 1/fps
        ending = False
        while ending == False:

            # Redraw every frame even if no event was incoming

            self.views[self.view].draw(screen, self.board, self.winning_rows)
            dt = fpsClock.tick(fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ending = True

                # Handle pygame event
                # Potentially move event to event manager

                result = self.views[self.view].handle_event(event, self.board)
                if result != None:
                    for event in result:
                        self.event_manager.Post(event)
