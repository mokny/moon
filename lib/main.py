import mokkalib

class Main():
    def __init__(self, database, httpserver, websocketserver):  
        self.database = database
        self.httpserver = httpserver
        self.websocketserver = websocketserver

        mokkalib.triggerGlobalEvent('INITIALIZED')
