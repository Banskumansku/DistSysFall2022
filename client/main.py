from view import ViewManager
from eventmanager import EventManager
from broadcast import Broadcaster
from controller import Controller
from server import Server

import sys

e = EventManager()

c = Controller({"MATCHMAKER": sys.argv[-1]})
c.set_event_manager(e)

b = Broadcaster()
b.set_event_manager(e)

v = ViewManager()
v.set_event_manager(e)

s = Server()
s.set_event_manager(e)
s.serve(8080)

e.StartNotifying()

v.main_game()
