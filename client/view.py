import pygame
import model

# draws different game views (start view, wait view, game view, game over view)


class MainView():

    def draw(self, screen):
        screen.fill((0, 0, 0))  # Fill the screen with black.

        # Redraw screen here.
        button1 = model.Button(
            "Start a new game",
            (100, 100),
            screen)
        screen.blit(button1.surface, (self.x, self.y))
        button1.click(event)

        # Flip the display so that the things we drew actually show up.
        pygame.display.flip()
        pygame.display.set_caption('Welcome to the game')
        pass

    def handle_event(self, event):
        button1.click(event)
        pass
        # if event.type == KEYUP:
        #  if event.key == K_a:
        #    scene = scenes['Battle']

    def update(self, dt):
        view = views['Main']


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

    def update(self, dt):
        # if opponent has been found:
        view = views['Game']


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

    def update(self, dt):
        # if game is over:
        view = views['GameEnd']


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

    def update(self, dt):
        # if player wants to play again
        view = views['Wait']


views = {'Main': MainView(),
         'Wait': WaitView(),
         'Game': GameView(),
         'GameEnd': GameEndView()}

view = views['Main']
clock = pygame.time.Clock()


def main_game():

    fps = 60.0
    fpsClock = pygame.time.Clock()

    width, height = 640, 480
    screen = pygame.display.set_mode((width, height))

    pygame.init()

    dt = 1/fps
    ending = False
    while ending == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ending = True
            view.handle_event(event)
            view.update(dt)
            view.draw(screen)

            dt = fpsClock.tick(fps)
