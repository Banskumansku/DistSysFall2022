import cherrypy
import threading

class Server():

    def __init__(self):
        self.running = threading.Lock()

    def serve(self, port):

        if not self.running.acquire(blocking=False):
            raise Exception("Server is already running")
        cherrypy.config.update({'server.socket_port': port})

        def subfunction():
            cherrypy.tree.graft(self.reply, '/')
            cherrypy.engine.start()

        t = threading.Thread(target=subfunction)
        t.start()

    def stop(self):
        cherrypy.engine.stop()
        self.running.release()
        
    def reply(self, environ, start_response):
        status = '200 OK'
        headers = [('Content-type', 'text/plain; charset=utf-8')]
        start_response(status, headers)

        return [f"Server is running".encode("utf-8")]
