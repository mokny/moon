import mokkalib

class Main():
    def __init__(self, database, webserver, websocketserver):  
        self.database = database
        self.webserver = webserver
        self.websocketserver = websocketserver

        mokkalib.triggerGlobalEvent('INITIALIZED')

