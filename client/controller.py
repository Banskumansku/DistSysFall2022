# contains game logic and handles messages with event manager

from eventmanager import ReplyEvent, ChangeViewEvent, RequestQueueEvent, BroadcastEvent, ReadBoardEvent, BoardClickedEvent, UpdateBoardEvent
import json
import model
from random import choice

class Controller():
    def __init__(self, context):
        self.player = None
        self.turn = None
        self.context = context
        self.state = "Main"

    def set_event_manager(self, event_manager):
        self.event_manager = event_manager
        self.event_manager.RegisterListener(self)

    def notify(self, event):

        print(f"Event reached controller: {event}") 

        # The player asked to be put on the queue

        if isinstance(event, RequestQueueEvent) and self.state == "Main":
            self.event_manager.Post(BroadcastEvent(self.context["MATCHMAKER"]+"/request-match",
                                                   json.dumps({"name": self.context["NAME"],
                                                               "id": None,
                                                                "return_url": self.context["RETURN_ADDRESS"]})))

        # The matchmaker told the client something about it getting on the queue

        if isinstance(event, ReplyEvent) and event.target.split("/")[-1] == "request-match" and self.state == "Main":
            if event.payload == {"status": "success"}:
                print("Got on queue successfully")
                self.state = "Wait"
                self.event_manager.Post(ChangeViewEvent("Wait"))
            else:
                print("Failed to get on queue")

        if isinstance(event, ReplyEvent) and event.target.split("/")[-1] == "matchmaking-success" and self.state == "Wait":
            print(f"Start game with players {event.payload}")
            self.turn = model.Ruutu.CROSS
            if self.context["RETURN_ADDRESS"] == event.payload[0]["return_url"]:
                self.player = model.Ruutu.CROSS
            else:
                self.player = model.Ruutu.NOUGHT
            self.state = "Game"
            self.event_manager.Post(ReadBoardEvent())
            self.event_manager.Post(ChangeViewEvent("Game"))

        if isinstance(event, BoardClickedEvent) and self.state == "Game" and self.player == self.turn:
            self.event_manager.Post(UpdateBoardEvent(event.x, event.y, self.player))
