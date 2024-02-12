#!/usr/bin/env python

import asyncio
import websockets
import http.server
import socketserver
import threading
import uuid
import json

def newHTTPServer(host, port, directory):
    s = HTTPServer(host, port, directory)
    s.start()
    return s

def newWebSocketServer(host, port, connectionhandler, messagehandler, disconnecthandler):  
    s = WebSocketServer(host, port, connectionhandler, messagehandler, disconnecthandler)
    s.start()
    return s

def msg(method, payload):
    return json.dumps({"m": method, "p": payload})

class WebSocketClient():
    def __init__(self, websocket, server):
        self.id = str(uuid.uuid4())
        self.websocket = websocket
        self.server = server

        self.disconnectflag = False
        self.create()

    def disconnect(self):
        self.disconnectflag = True

    def create(self):
        self.server.clients[self.id] = self
        self.server.connections.add(self.websocket)

    def remove(self):
        del self.server.clients[self.id]
        self.server.connections.remove(self.websocket)

    async def send(self, method, payload):
        await self.websocket.send(msg(method, payload))


class WebSocketServer(threading.Thread):
    def __init__(self, host, port, connectionhandler, messagehandler, disconnecthandler):  
        print("Initializing WS Server") 
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.connectionhandler = connectionhandler
        self.messagehandler = messagehandler
        self.disconnecthandler = disconnecthandler

        self.connections = set()
        self.clients = {}
        
        self.connections_max = 100              # maximum allowed connections
        self.connections_accept = True          # generally accept new connections

    def setMaxConnections(self, max):
        self.connections_max = max

    def setAcceptNewConnections(self, value):
        self.connections_accept = value

    # Broadcast to all clients
    async def broadcast(self, method, payload):
        websockets.broadcast(self.connections, msg(method, payload))

    async def newconnection(self, websocket):
        if not self.connections_accept: return
        if len(self.connections) >= self.connections_max: return

        client = WebSocketClient(websocket, self)
        try:
            await self.connectionhandler(self, client)
            async for raw in websocket:
                message = json.loads(raw)
                await self.messagehandler(self, client, message['m'], message['p'])
                if client.disconnectflag: break

        finally:
            client.remove()
            await self.disconnecthandler(self, client)
            

    async def startserver(self):
        async with websockets.serve(self.newconnection, self.host, self.port):
            await asyncio.Future()

    def run(self): 
        asyncio.run(self.startserver())  



class HTTPServer(threading.Thread):
    def __init__(self, host, port, directory):  
        print("Initializing HTTP Server") 
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.directory = directory
        self.server = None

    def run(self):   
        print("Starting HTTP Server") 

        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory='www', **kwargs)

        with socketserver.TCPServer((self.host, self.port), Handler) as self.httpd:
            print("serving at port", self.port)
            try:
                self.httpd.serve_forever()
            except KeyboardInterrupt:
                print("http shutdown")
                self.httpd.shutdown()
        self.httpd.shutdown()
    
    def kill(self):
        self.httpd.shutdown()