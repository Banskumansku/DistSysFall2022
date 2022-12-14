import cherrypy
import threading
from queue import Queue
import requests
import json

class MockServer():

    def __init__(self):
        self.queue = Queue()

        t = threading.Thread(target=self.consume_queue)
        t.start()

        cherrypy.config.update({'server.socket_port': 1337})

        cherrypy.tree.graft(self.reply, '/')
        cherrypy.engine.start()

    def consume_queue(self):
        while True:
            match = []
            for _ in range(2):
                match.append(self.queue.get())

            # Match is made

            data = {"opponents": []}

            for player in match:
                data["opponents"].append({"name": player["name"], "return_url": player["return_url"]})

            for player in match:
                target_url = player["return_url"]+"/matchmaking-success"
                payload = json.dumps(data)
                print("POSTing to " + target_url + ":" + payload)
                requests.post(target_url, payload)
        

    def reply(self, environ, start_response):
        print("PATH_INFO", environ["PATH_INFO"])
        print("REQUEST_METHOD", environ["REQUEST_METHOD"])
        data = json.loads(environ["wsgi.input"].read())
        print("wsgi.input", data)
        if environ["PATH_INFO"] == "/request-match" and environ["REQUEST_METHOD"] == "POST":
            self.queue.put(data)
            status = '200 OK'
            headers = [('Content-type', 'application/json; charset=utf-8')]
            start_response(status, headers)
            return ['{"status":"success"}'.encode("utf-8"),]


        status = '404 NOT FOUND'
        headers = [('Content-type', 'application/json; charset=utf-8')]
        start_response(status, headers)
        return ['{"error": "not found"}'.encode("utf-8"),]

MockServer()
