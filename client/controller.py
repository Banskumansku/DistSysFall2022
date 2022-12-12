# contains game logic and handles messages with event manager

from eventmanager import ReplyEvent, ChangeViewEvent, RequestQueueEvent, BroadcastEvent
import json

class Controller():
    def __init__(self, context):
        self.context = context

    def set_event_manager(self, event_manager):
        self.event_manager = event_manager
        self.event_manager.RegisterListener(self)

    def notify(self, event):

        print(f"Event reached controller: {event}") 

        # The player asked to be put on the queue

        if isinstance(event, RequestQueueEvent):
            self.event_manager.Post(BroadcastEvent(self.context["MATCHMAKER"]+"/request-match",
                                                   json.dumps({"name": self.context["NAME"],
                                                               "id": None,
                                                                "return_url": self.context["RETURN_ADDRESS"]})))

        # The matchmaker told the client something about it getting on the queue

        if isinstance(event, ReplyEvent) and event.target.split("/")[-1] == "request-match":
            if event.payload == {"status": "success"}:
                print("Got on queue successfully")
                self.event_manager.Post(ChangeViewEvent("Wait"))
            else:
                print("Failed to get on queue")

        if isinstance(event, ReplyEvent) and event.target.split("/")[-1] == "matchmaking-success":
            print(f"Start game with players {event.payload}")
            self.event_manager.Post(ChangeViewEvent("Game"))
