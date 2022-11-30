import pygame

# draws different game views (start view, wait view, game view, game over view)

class MainView():
    def handle_event(self, event):
        pass
        # if event.type == KEYUP:
        #  if event.key == K_a:
        #    scene = scenes['Battle']


class WaitView():
    def draw(self):
        # draw your animation
        pass

    def update(self):
        # if opponent has been found:
        view = views['Game']


class GameView():
    def draw(self):
        # draw your animation
        pass

    def update(self):
        # if game is over:
        view = views['GameEnd']


class GameEndView():
    def draw(self):
        pass

    def update(self):
        # if player wants to play again
        view = views['Wait']

views = {'Main': MainView(),
         'Wait': WaitView(),
         'Game': GameView(),
         'GameEnd': GameEndView()}

view = views['Main']
clock = pygame.time.Clock()

def main_game():
    ending = False
    while ending == False:
        clock.tick(30)
        for event in pygame.event.get():
            view.handle_event(event)
            view.update()
            view.draw()