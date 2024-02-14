import mokkalib

class Main():
    def __init__(self, database, webserver, websocketserver):  
        self.database = database
        self.webserver = webserver
        self.websocketserver = websocketserver

        self.webserver.addscriptvar('websocket.host', self.websocketserver.host)
        self.webserver.addscriptvar('websocket.port', self.websocketserver.port)

        mokkalib.triggerGlobalEvent('INITIALIZED')

