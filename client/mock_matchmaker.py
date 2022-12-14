# Matchmaker in-lieu of the nodejs implementation

import cherrypy # <- server middleware
import threading
from queue import Queue
import requests # <- making http POST requests outwards
import json

class MockServer():

    def __init__(self):

        # The queue of players

        self.queue = Queue()

        # Have another thread ready to broadcast news of matches being made

        t = threading.Thread(target=self.consume_queue)
        t.start()

        # Reply to everyone (=0.0.0.0); work on port 1337

        cherrypy.config.update({'server.socket_port': 1337})
        cherrypy.config.update({'server.socket_host': '0.0.0.0'})

        # Hook up the reply function to cherrypy & start server

        cherrypy.tree.graft(self.reply, '/')
        cherrypy.engine.start()

    def consume_queue(self):

        # Endlessly spin for new matches

        while True:

            # Get two players off the queue

            match = []
            for _ in range(2):
                match.append(self.queue.get()) # <- blocking

            # Collect data on the opponents into a dictionary

            data = {"opponents": []}
            for player in match:
                data["opponents"].append({"name": player["name"], "return_url": player["return_url"]})

            # Broadcast the data to the players

            for player in match:
                target_url = player["return_url"]+"/matchmaking-success"
                payload = json.dumps(data)
                print("POSTing to " + target_url + ":" + payload)
                requests.post(target_url, payload)


    # Server functionality

    def reply(self, environ, start_response):

        # Debug info

        print("PATH_INFO", environ["PATH_INFO"])
        print("REQUEST_METHOD", environ["REQUEST_METHOD"])
        data = json.loads(environ["wsgi.input"].read()) # (read is destructive)
        print("wsgi.input", data)

        # Handle asking to be put on the queue

        if environ["PATH_INFO"] == "/request-match" and environ["REQUEST_METHOD"] == "POST":
            self.queue.put(data)
            status = '200 OK'
            headers = [('Content-type', 'application/json; charset=utf-8')]
            start_response(status, headers)
            return ['{"status":"success"}'.encode("utf-8"),]

        # Something else was asked for; 404, could arguably be 400

        status = '404 NOT FOUND'
        headers = [('Content-type', 'application/json; charset=utf-8')]
        start_response(status, headers)
        return ['{"error": "not found"}'.encode("utf-8"),]

# Start the server

MockServer()
