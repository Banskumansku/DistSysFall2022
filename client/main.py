from view import ViewManager
from eventmanager import EventManager
from broadcast import Broadcaster
from controller import Controller
from server import Server

import sys


try:
    context = {"MATCHMAKER": sys.argv[1], "RETURN_ADDRESS": sys.argv[2], "NAME": sys.argv[3], "PORT": int(sys.argv[2].split(":")[2])}
except IndexError:
    print("usage: main.py <matchmaker address> <return address> <name>")
    sys.exit(1)

e = EventManager()

c = Controller(context)
c.set_event_manager(e)

b = Broadcaster()
b.set_event_manager(e)

v = ViewManager()
v.set_event_manager(e)

s = Server()
s.set_event_manager(e)
s.serve(context["PORT"])

e.StartNotifying()

v.main_game()
