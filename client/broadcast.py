from eventmanager import EventManager, BroadcastEvent, ReplyEvent
import requests

class Broadcaster():
    def __init__(self):
        pass

    def set_event_manager(self, event_manager):
        self.event_manager = event_manager
        self.event_manager.RegisterListener(self)

    def notify(self, event):
        if isinstance(event, BroadcastEvent):
            print("--- Commence broadcast ---")
            print(f"Target: {event.target}")
            print(f"Payload: {event.payload}")
            print("------ End broadcast -----")
            print("----- Commence reply -----")
            try:
                result = requests.post(event.target, event.payload).text
            except:
                result = None
            print(result)
            print("------- End reply --------")
            self.event_manager.Post(ReplyEvent(event.target, result))
