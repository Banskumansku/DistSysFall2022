import pygame
import model
from eventmanager import EventManager, ChangeViewEvent, RequestQueueEvent
from broadcast import Broadcaster
import time

# draws different game views (start view, wait view, game view, game over view)


class MainView():

    def __init__(self):
        self.button1 = model.Button(
            "Start a new game",
            (100, 100),
            16)

    def draw(self, screen):
        screen.fill((0, 0, 0))  # Fill the screen with black.

        # Redraw screen here
        self.button1.show(screen)

        # Flip the display so that the things we drew actually show up.
        pygame.display.flip()
        pygame.display.set_caption('Welcome to the game')
        pass

    def handle_event(self, event):
        if event.type == 1026 and self.button1.is_within_bounds(event.pos[0], event.pos[1]):
            return [RequestQueueEvent()]


class WaitView():
    def draw(self, screen):
        screen.fill((255, 0, 0))  # Fill the screen with red.

        # Redraw screen here.

        # Flip the display so that the things we drew actually show up.
        pygame.display.flip()
        pygame.display.set_caption('Waiting for your opponent')
        # draw your animation
        pass

    def handle_event(self, event):
        pass


class GameView():
    def draw(self, screen):
        screen.fill((0, 255, 0))  # Fill the screen with green.

        # Redraw screen here.

        # Flip the display so that the things we drew actually show up.
        pygame.display.flip()
        pygame.display.set_caption('Game view')
        # draw your animation
        pass

    def handle_event(self, event):
        pass

class GameEndView():
    def draw(screen):
        screen.fill((0, 0, 255))  # Fill the screen with blue.

        # Redraw screen here.

        # Flip the display so that the things we drew actually show up.
        pygame.display.flip()
        pygame.display.set_caption('Game over')
        pass

    def handle_event(self, event):
        pass

class ViewManager():

    def __init__(self):
        self.views = {'Main': None,
                      'Wait': None,
                      'Game': None,
                      'GameEnd': None}
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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ending = True

                # Handle pygame event
                # Potentially move event to event manager

                result = self.views[self.view].handle_event(event)
                if result != None:
                    for event in result:
                        self.event_manager.Post(event)

                self.views[self.view].draw(screen)

                dt = fpsClock.tick(fps)
