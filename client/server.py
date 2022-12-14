import cherrypy
import threading
import json
from eventmanager import EventManager, QuitEvent, ReplyEvent

class Server():

    def __init__(self):
        self.running = threading.Lock()

    def set_event_manager(self, event_manager):
        self.event_manager = event_manager
        self.event_manager.RegisterListener(self)

    def notify(self, event):
        if isinstance(event, QuitEvent):
            self.stop()

    def serve(self, port):

        if not self.running.acquire(blocking=False):
            raise Exception("Server is already running")
        cherrypy.config.update({'server.socket_port': port})
        cherrypy.config.update({'server.socket_host': '0.0.0.0'})

        def subfunction():
            cherrypy.tree.graft(self.reply, '/')
            cherrypy.engine.start()

        t = threading.Thread(target=subfunction)
        t.start()

    def stop(self):
        cherrypy.engine.stop()
        self.running.release()
        
    def reply(self, environ, start_response):
        if environ["PATH_INFO"] == "/matchmaking-success" and environ["REQUEST_METHOD"] == "POST":

            # Matchmaking is succeeding, yay

            try:

                # TODO: Very light validation so far

                opponents = json.loads(environ['wsgi.input'].read().decode("utf-8"))["opponents"]
                self.event_manager.Post(ReplyEvent("//matchmaking-success", opponents))
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

                # TODO: Very light validation so far

                history = json.loads(environ['wsgi.input'].read().decode("utf-8"))
                self.event_manager.Post(ReplyEvent("//make-move", history))
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
            status = "404 NOT FOUND"
            headers = [('Content-type', 'application/json; charset=utf-8')]
            start_response(status, headers)

            return ['{"error":"not found"}'.encode("utf-8")]
