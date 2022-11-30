# ---- Palvelin ----

from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server

import threading
import time

class Palvelin():

    def __init__(self):
        self.counter = 0

    def palvele(self, portti):
        def alifunktio():
            with make_server('', portti, self.simple_app) as httpd:
                print(f"Palvellaan portilla {portti}")
                httpd.serve_forever()
        t = threading.Thread(target=alifunktio)
        t.start()

    def simple_app(self, environ, start_response):

        setup_testing_defaults(environ)

        status = '200 OK'
        headers = [('Content-type', 'text/plain; charset=utf-8')]

        start_response(status, headers)

        self.counter += 1 # Ei atominen, ei synkkaava

        return [f"Sivulla käyty {self.counter} kertaa".encode("utf-8")]

p = Palvelin()
p.palvele(8000) # -> Aloittaa oman säikeensä

# ---- PyGame ----

import sys

import pygame
from pygame.locals import *

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

width, height = 640, 480
screen = pygame.display.set_mode((width, height))

i = 0

# Game loop.
while True:
  screen.fill((i, 0, 0))

  i = (i + 1) % 255

  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()

  for x in range(p.counter):
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect((640//2-5, 480//2-5+x*15), (10, 10)))

  # Update.

  # Draw.

  pygame.display.flip()
  fpsClock.tick(fps)
