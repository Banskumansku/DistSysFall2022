import cherrypy

def reply(environ, start_response):
    if environ["PATH_INFO"] == "/request-match" and environ["REQUEST_METHOD"] == "POST":
        status = '200 OK'
        headers = [('Content-type', 'text/plain; charset=utf-8')]
        start_response(status, headers)
        return ["success".encode("utf-8"),]


    status = '404 NOT FOUND'
    headers = [('Content-type', 'text/plain; charset=utf-8')]
    start_response(status, headers)
    return ["Not Found".encode("utf-8"),]

cherrypy.config.update({'server.socket_port': 1337})

cherrypy.tree.graft(reply, '/')
cherrypy.engine.start()
