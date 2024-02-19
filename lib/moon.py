import mokkalib
import socket

class Moon():
    def __init__(self, database, webserver, websocketserver):  
        self.database = database
        self.webserver = webserver
        self.websocketserver = websocketserver

        # Set Script variables for the webserver.
        hostname = self.websocketserver.host
        if hostname == '0.0.0.0': hostname = socket.gethostname()
        self.webserver.setscriptvar('websocket.host', hostname)

        self.webserver.setscriptvar('websocket.port', self.websocketserver.port)

        

        mokkalib.triggerGlobalEvent('INITIALIZED')

