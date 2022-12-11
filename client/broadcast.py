from eventmanager import EventManager, BroadcastEvent
import requests

class Broadcaster():
    def __init__(self):
        pass

    def notify(self, event):
        if isinstance(event, BroadcastEvent):
            print("--- Commence broadcast ---")
            print(f"Target: {event.target}")
            print(f"Payload: {event.payload}")
            print("------ End broadcast -----")
            print("----- Commence reply -----")
            print(requests.post(event.target, event.payload).text)
            print("------- End reply --------")
