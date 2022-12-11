from eventmanager import EventManager, QuitEvent, BroadcastEvent
from server import Server
from broadcast import Broadcaster

class CliListener():
    def __init__(self):
        print("CLI listener started")

    def notify(self, event):
        print(f"Incoming event: {event}")

e = EventManager()

s = Server()
s.set_event_manager(e)
e.RegisterListener(CliListener())
s.serve(8080)

b = Broadcaster()
e.RegisterListener(b)

e.StartNotifying()

while True:
    i = input("> ")
    if i == "quit":
        e.Post(QuitEvent())
    if i.split(" ")[0] == "broadcast":
        e.Post(BroadcastEvent(i.split(" ")[1], i.split(" ")[2]))
