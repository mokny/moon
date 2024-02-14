#!/usr/bin/env python

import asyncio
import websockets
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import uuid
import json
import time
import signal
import os
import mimetypes
import re
from functools import partial

def newWebServer(host, port, directory):
    s = WebServer(host, port, directory)
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
        self.path = self.websocket.path
        self.ip = self.websocket.remote_address[0]
        
        self.data = {}  # Stores all external data for this client
        
        self.timestamp_connect = int(time.time())
        self.timestamp_lastmessage = int(time.time())
        self.timestamp_pingtest = 0
        self.timestamp_nextping = int(time.time())

        self.pinginterval = 5

        self.latency = 0
        self.disconnectflag = False
        self.create()

    def disconnect(self):
        self.disconnectflag = True

    def secondsConnected(self):
        return int(time.time()) - self.timestamp_connect

    def secondsIdle(self):
        return int(time.time()) - self.timestamp_lastmessage

    def create(self):
        self.server.clients[self.id] = self
        self.server.connections.add(self.websocket)

    def remove(self):
        del self.server.clients[self.id]
        self.server.connections.remove(self.websocket)

    async def send(self, method, payload):
        await self.websocket.send(msg(method, payload))

    async def ping(self):
        if self.timestamp_nextping > int(time.time()): return
        self.timestamp_pingtest = round(time.time() * 1000)
        self.timestamp_nextping = round(time.time()) + self.pinginterval
        await self.send('XPING', self.timestamp_pingtest)

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

        await client.ping()

        try:
            await self.connectionhandler(self, client)
            async for raw in websocket:
                client.timestamp_lastmessage = int(time.time())
                message = json.loads(raw)
                await client.ping()
                if message['m'] == 'XPING':
                    await client.send('XPONG', message['p'])
                elif message['m'] == 'XPONG':
                    client.latency = round(time.time() * 1000) - client.timestamp_pingtest
                    await client.send('XLAT', client.latency)
                else:
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



class WebServer(threading.Thread):
    def __init__(self, host, port, directory):  
        print("Initializing WebServer") 
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.directory = directory
        self.server = None
        self.scriptvars = {}

        signal.signal(signal.SIGTERM, self.sigterm_handler)  

    def sigterm_handler(self,_signo, _stack_frame):
        self.kill()

    def run(self): 
        class Handler(SimpleHTTPRequestHandler):
            def __init__(self, webserver, *args, **kwargs):
                self.webserver = webserver
                super().__init__(*args, **kwargs)

            def do_GET(self):
                if self.path == '/': self.path = '/index.html'
                mimetype = mimetypes.guess_type(self.path)

                if os.path.isfile('www' + self.path):
                    self.send_response(200)

                    if self.path.lower().endswith('.html') or self.path.lower().endswith('.htm'):
                        self.send_header("Content-Type", 'text/html')
                    elif self.path.lower().endswith('.css'):
                        self.send_header("Content-Type", 'text/css')
                    elif self.path.lower().endswith('.js'):
                        self.send_header("Content-Type", 'text/javascript')
                    else:
                        self.send_header("Content-Type", mimetype)

                    self.end_headers()
                    
                    if self.path.lower().endswith('.html') or self.path.lower().endswith('.htm') or self.path.lower().endswith('.js'):
                        f = open('www' + self.path, "r")
                        content = f.read()
                        scripts = re.findall(r'\{\{.*?\}\}', content)
                        for script in scripts:
                            result = self.webserver.parsescript(script)
                            content = content.replace(script, result)

                        self.wfile.write(bytes(content,'utf-8')) 
                    else:
                        with open('www' + self.path, 'rb') as file: 
                            self.wfile.write(file.read())   
                else:
                    self.send_response(404)
                    self.end_headers()     

        self.webhandler = partial(Handler, self)
        self.server = HTTPServer((self.host, self.port), self.webhandler)
        thread = threading.Thread(target = self.server.serve_forever)
        thread.daemon = True
        thread.start() 

    def setscriptvar(self, var, value):
        self.scriptvars[var] = value

    def getscriptvar(self, var, default='nothing'):
        if var in self.scriptvars:
            return str(self.scriptvars[var])
        else:
            return str(default)

    def parsescript(self, script):
        if str(script).startswith('{{%') and str(script).endswith('%}}'):
            script = script.replace('{{%','',1)
            script = script[::-1]
            script = script.replace('}}%','',1)
            script = script[::-1]
            lines = script.split(';')
            result = ''
            for line in lines:
                try:
                    spl = line.strip().split(' ', 1)
                    method = spl[0]

                    if method == 'echo':
                        result += spl[1]

                    if method == 'get':
                        result += self.getscriptvar(spl[1])

                    if method == 'template':
                        f = open(spl[1], "r")
                        tplcontent = f.read()
                        tplscripts = re.findall(r'\{\{.*?\}\}', tplcontent)
                        for tplscript in tplscripts:
                            tplresult = self.parsescript(tplscript)
                            tplcontent = tplcontent.replace(tplscript, tplresult)
                        result += tplcontent

                    if method == 'timestamp':
                        result += str(int(time.time()))

                except:
                    result += 'error'
                    pass
            return result
        else:
            return script    
        
    def kill(self):
        print("Shutting down WebServer") 
        self.server.shutdown()

