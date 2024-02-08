import websockets
import threading

class server(threading.Thread):
    def __init__(self, host, port, directory):  
        print("Initializing Websocket Server") 
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.directory = directory

    def run(self):   
        print("Starting Websocket Server") 

