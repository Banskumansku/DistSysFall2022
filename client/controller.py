# Contains most of the game logic and handles messages with event manager
# The model contains the state of the board and deals with wins/losses

# Need a wide variety of event types

from eventmanager import ReplyEvent, ChangeViewEvent, RequestQueueEvent, BroadcastEvent, ReadBoardEvent, BoardClickedEvent, UpdateBoardEvent, BoardStateEvent, ResetViewEvent, ResetBoardEvent
import json
import model

class Controller():
    def __init__(self, context):
        self.player = None # noughts, crosses or None
        self.history = None # what moves have been player
        self.opponent = None # url of opponent
        self.over = False # is the game ongoing or won/lost/drawn
        self.context = context # info about matchmaker and own address
        self.state = "Main" # roughlt the current view

    # Register and get a handle on the event manager

    def set_event_manager(self, event_manager):
        self.event_manager = event_manager
        self.event_manager.RegisterListener(self)

    def notify(self, event):

        print(f"Event reached controller: {event}") 

        # The player asked to be put on the queue

        if isinstance(event, RequestQueueEvent) and self.state == "Main":
            self.event_manager.Post(BroadcastEvent(self.context["MATCHMAKER"]+"/request-match",
                                                   {"name": self.context["NAME"],
                                                    "id": None,
                                                    "return_url": self.context["RETURN_ADDRESS"]}))

        # The matchmaker told the client something about it getting on the queue

        if isinstance(event, ReplyEvent) and event.target.split("/")[-1] == "request-match" and self.state == "Main":
            if event.payload == {"status": "success"}:
                print("Got on queue successfully")
                self.state = "Wait"
                self.event_manager.Post(ChangeViewEvent("Wait"))
            else:
                print("Failed to get on queue")

        # The player got on the queue

        if isinstance(event, ReplyEvent) and event.target.split("/")[-1] == "matchmaking-success" and self.state == "Wait":
            print(f"Start game with players {event.payload}")

            # A lot of initial state setting

            self.history = []
            self.own_index = 0
            if self.context["RETURN_ADDRESS"] == event.payload[0]["url"]:
                self.player = model.Ruutu.CROSS
            else:
                self.player = model.Ruutu.NOUGHT
                self.own_index = 1
            self.opponent = event.payload[(self.own_index+1)%2]["url"]
            self.state = "Game"
            self.over = False
            self.last_confirmed = 0
            self.event_manager.Post(ResetBoardEvent())
            self.event_manager.Post(ReadBoardEvent())
            self.event_manager.Post(ChangeViewEvent("Game"))

        # Handle race condition, where a player clicks while a network request that wins the game is being processed, thus getting in a move into an empty square after the game is over

        if isinstance(event, BoardClickedEvent) and self.state == "Game" and self.last_confirmed != len(self.history):
            self.event_manager.post(event) # Bump to back of queue; can't tell if board is in winning state
            return

        # Handle a player clicking a square

        if isinstance(event, BoardClickedEvent) and self.state == "Game" and self.own_index == len(self.history) % 2 and [event.x, event.y] not in self.history and self.over == False:
            self.history.append([event.x, event.y])
            self.event_manager.Post(UpdateBoardEvent(event.x, event.y, self.player))
            self.event_manager.Post(BroadcastEvent(self.opponent+"/make-move", self.history))

        # Handle move coming in over network
        
        if isinstance(event, ReplyEvent) and event.target.split("/")[-1] == "make-move" and self.state == "Game" and self.over == False:
            if len(event.payload) == len(self.history)+1:
                move = event.payload[-1]
                if event.payload[:-1] == self.history and move not in self.history:
                    self.history.append(move)
                    other = model.Ruutu.CROSS
                    if self.player == model.Ruutu.CROSS:
                        other = model.Ruutu.NOUGHT
                    self.event_manager.Post(UpdateBoardEvent(move[0], move[1], other))

        # Handle the model telling us something about the board state

        if isinstance(event, BoardStateEvent) and self.state == "Game":
            qty = 0
            for y in range(3):
                for x in range(3):
                    if event.payload[y][x] != model.Ruutu.EMPTY:
                        qty += 1
            self.last_confirmed = qty
            if event.winning_rows != [] or qty == 9:
                self.over = True
            if self.over:
                self.event_manager.Post(ChangeViewEvent("GameEnd"))
                self.state = "GameEnd"

        # Handle the user re-setting the game after the game is over

        if isinstance(event, ResetViewEvent) and self.state == "GameEnd":
            self.event_manager.Post(ChangeViewEvent("Main"))
            self.state = "Main"
