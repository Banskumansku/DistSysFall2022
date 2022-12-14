import cherrypy # server middleware
import threading
import json

# Import relevant events

from eventmanager import EventManager, QuitEvent, ReplyEvent

class Server():

    def __init__(self):
        self.running = threading.Lock() # Use a lock to avoid double launch

    # Register to the event manager and keep a handle on it

    def set_event_manager(self, event_manager):
        self.event_manager = event_manager
        self.event_manager.RegisterListener(self)

    # Only react to a quit events (not used as of writing)

    def notify(self, event):
        if isinstance(event, QuitEvent):
            self.stop()

    def serve(self, port):

        # If not running, start on specified port and all interfaces

        if not self.running.acquire(blocking=False):
            raise Exception("Server is already running")
        cherrypy.config.update({'server.socket_port': port})
        cherrypy.config.update({'server.socket_host': '0.0.0.0'})

        # Song and dance to launch server in separate thread

        def subfunction():
            cherrypy.tree.graft(self.reply, '/')
            cherrypy.engine.start()

        t = threading.Thread(target=subfunction)
        t.start()

    def stop(self):
        cherrypy.engine.stop()
        self.running.release()
        
    def reply(self, environ, start_response):

        # The matchmaker told us we got matched

        if environ["PATH_INFO"] == "/matchmaking-success" and environ["REQUEST_METHOD"] == "POST":

            # Matchmaking is succeeding, yay

            try:

                # Not much validation; trusted source

                opponents = json.loads(environ['wsgi.input'].read().decode("utf-8"))["opponents"]
                self.event_manager.Post(ReplyEvent("//matchmaking-success", opponents)) # Inform rest of world
            except (json.decoder.JSONDecodeError, KeyError):

                # Garbage data

                status = '400 BAD REQUEST'
                headers = [('Content-type', 'application/json; charset=utf-8')]
                start_response(status, headers)

                return ['{"error": "bad request"}'.encode("utf-8")]

            status = '200 OK'
            headers = [('Content-type', 'application/json; charset=utf-8')]
            start_response(status, headers)

            return ['{"status": "success"}'.encode("utf-8")]

        if environ["PATH_INFO"] == "/make-move" and environ["REQUEST_METHOD"] == "POST":
           
            # A move was made, yay

            try:

                # Again, trusted source

                history = json.loads(environ['wsgi.input'].read().decode("utf-8"))
                self.event_manager.Post(ReplyEvent("//make-move", history)) # Inform rest of world
            except (json.decoder.JSONDecodeError, KeyError):

                # Garbage data

                status = '400 BAD REQUEST'
                headers = [('Content-type', 'application/json; charset=utf-8')]
                start_response(status, headers)

                return ['{"error": "bad request"}'.encode("utf-8")]
            status = '200 OK'
            headers = [('Content-type', 'application/json; charset=utf-8')]
            start_response(status, headers)

            return ['{"status": "success"}'.encode("utf-8")]
        else:

            # Nonsense request; could arguably be 400 too

            status = "404 NOT FOUND"
            headers = [('Content-type', 'application/json; charset=utf-8')]
            start_response(status, headers)

            return ['{"error":"not found"}'.encode("utf-8")]
