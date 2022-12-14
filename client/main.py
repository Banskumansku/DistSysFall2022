# Import all the disparate part of the system

from view import ViewManager
from eventmanager import EventManager
from broadcast import Broadcaster
from controller import Controller
from server import Server
from model import Model

# Read cli parameters

import sys
try:
    context = {"MATCHMAKER": sys.argv[1], "RETURN_ADDRESS": sys.argv[2], "NAME": sys.argv[3], "PORT": int(sys.argv[2].split(":")[2])}
except IndexError:
    print("usage: main.py <matchmaker address> <return address> <name>")
    sys.exit(1)

# - Initialize the various parts of the program
# - Hook them up to the event manager

e = EventManager()

c = Controller(context)
c.set_event_manager(e)

b = Broadcaster()
b.set_event_manager(e)

v = ViewManager()
v.set_event_manager(e)

m = Model()
m.set_event_manager(e)

s = Server()
s.set_event_manager(e)

# Start the server

s.serve(context["PORT"])

# Start the event manager's loop

e.StartNotifying()

# Launch the Pygame part of the game

v.main_game()
