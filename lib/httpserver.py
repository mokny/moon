import http.server
import socketserver
import threading



class server(threading.Thread):
    def __init__(self, host, port, directory):  
        print("Initializing HTTP Server") 
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.directory = directory

    def run(self):   
        print("Starting HTTP Server") 

        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory='www', **kwargs)


        with socketserver.TCPServer((self.host, self.port), Handler) as httpd:
            print("serving at port", self.port)
            httpd.serve_forever()