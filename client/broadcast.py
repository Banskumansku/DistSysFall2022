# The broadcaster is in charge of making requests outwards
# In a more real-worldey implementation: handle multicasting

from eventmanager import EventManager, BroadcastEvent, ReplyEvent
import requests

class Broadcaster():
    def __init__(self):
        pass

    # Register and get a handle on the event manager

    def set_event_manager(self, event_manager):
        self.event_manager = event_manager
        self.event_manager.RegisterListener(self)

    def notify(self, event):

        # Only react to BroadcastEvents

        if isinstance(event, BroadcastEvent):
            print("--- Commence broadcast ---")
            print(f"Target: {event.target}")
            print(f"Payload: {event.payload}")
            print("------ End broadcast -----")
            print("----- Commence reply -----")

            # Catch network errors

            try:
                result = requests.post(event.target, json=event.payload).json()
            except: # <- bad form, but justified by variety of potential errors
                result = None

            print(result)
            print("------- End reply --------")

            # Tell the event system of whatever the other end said

            self.event_manager.Post(ReplyEvent(event.target, result))
