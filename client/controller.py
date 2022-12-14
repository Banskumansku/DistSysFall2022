# contains game logic and handles messages with event manager

from eventmanager import ReplyEvent, ChangeViewEvent, RequestQueueEvent, BroadcastEvent, ReadBoardEvent, BoardClickedEvent, UpdateBoardEvent
import json
import model
from random import choice

class Controller():
    def __init__(self, context):
        self.player = None
        self.history = None
        self.opponent = None
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
            self.history = []
            self.own_index = 0
            if self.context["RETURN_ADDRESS"] == event.payload[0]["return_url"]:
                self.player = model.Ruutu.CROSS
            else:
                self.player = model.Ruutu.NOUGHT
                self.own_index = 1
            self.opponent = event.payload[(self.own_index+1)%2]["return_url"]
            self.state = "Game"
            self.event_manager.Post(ReadBoardEvent())
            self.event_manager.Post(ChangeViewEvent("Game"))

        if isinstance(event, BoardClickedEvent) and self.state == "Game" and self.own_index == len(self.history) % 2 and [event.x, event.y] not in self.history:
            self.history.append([event.x, event.y])
            self.event_manager.Post(UpdateBoardEvent(event.x, event.y, self.player))
            self.event_manager.Post(BroadcastEvent(self.opponent+"/make-move", json.dumps(self.history)))

        
        if isinstance(event, ReplyEvent) and event.target.split("/")[-1] == "make-move" and self.state == "Game":
            if len(event.payload) == len(self.history)+1:
                move = event.payload[-1]
                if event.payload[:-1] == self.history and move not in self.history:
                    self.history.append(move)
                    other = model.Ruutu.CROSS
                    if self.player == model.Ruutu.CROSS:
                        other = model.Ruutu.NOUGHT
                    self.event_manager.Post(UpdateBoardEvent(move[0], move[1], other))
