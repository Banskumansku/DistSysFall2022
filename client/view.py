import pygame
import model
from eventmanager import EventManager, ChangeViewEvent, BroadcastEvent
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
            return [ChangeViewEvent("Wait"), BroadcastEvent("http://localhost", '{"name":"test", "id":"1", "Pikku kakkosen posti"}')]


class WaitView():
    def draw(self, screen):
        screen.fill((0, 0, 0))  # Fill the screen with black.

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
        screen.fill((0, 0, 0))  # Fill the screen with black.

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
        screen.fill((0, 0, 0))  # Fill the screen with black.

        # Redraw screen here.

        # Flip the display so that the things we drew actually show up.
        pygame.display.flip()
        pygame.display.set_caption('Game over')
        pass

    def handle_event(self, event):
        pass

clock = pygame.time.Clock()

class ViewManager():
    def __init__(self):

        self.views = {'Main': MainView(),
                      'Wait': WaitView(),
                      'Game': GameView(),
                      'GameEnd': GameEndView()}
        self.view = self.views["Main"]

    def notify(self, event):
        if isinstance(event, ChangeViewEvent):
            self.view = self.views[event.view]

def main_game():

    fps = 60.0
    fpsClock = pygame.time.Clock()

    width, height = 640, 480
    screen = pygame.display.set_mode((width, height))

    pygame.init()

    e = EventManager()
    e.StartNotifying()

    v = ViewManager()
    e.RegisterListener(v)

    b = Broadcaster()
    e.RegisterListener(b)

    dt = 1/fps
    ending = False
    while ending == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ending = True

            # Handle pygame event
            # Potentially move event to event manager

            result = v.view.handle_event(event)
            if result != None:
                for event in result:
                    e.Post(event)

            v.view.draw(screen)

            dt = fpsClock.tick(fps)
