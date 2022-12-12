import cherrypy

def reply(environ, start_response):
    print("PATH_INFO", environ["PATH_INFO"])
    print("REQUEST_METHOD", environ["REQUEST_METHOD"])
    print("wsgi.input", environ["wsgi.input"].read())
    if environ["PATH_INFO"] == "/request-match" and environ["REQUEST_METHOD"] == "POST":
        status = '200 OK'
        headers = [('Content-type', 'application/json; charset=utf-8')]
        start_response(status, headers)
        return ['{"status":"success"}'.encode("utf-8"),]


    status = '404 NOT FOUND'
    headers = [('Content-type', 'application/json; charset=utf-8')]
    start_response(status, headers)
    return ['{"error": "not found"}'.encode("utf-8"),]

cherrypy.config.update({'server.socket_port': 1337})

cherrypy.tree.graft(reply, '/')
cherrypy.engine.start()
