#!/usr/bin/env python

import asyncio
import websockets
import datetime
import random
import threading
import uuid
import json
import vars as v

def msg(method, payload):
    return json.dumps({"m": method, "p": payload})


class User():
    def __init__(self, websocket):
        self.id = str(uuid.uuid4())
        self.websocket = websocket
        self.create()

    def create(self):
        v.users[self.id] = self
        v.connections.add(self.websocket)

    def remove(self):
        del v.users[self.id]
        v.connections.remove(self.websocket)

    async def send(self, method, payload):
        await self.websocket.send(msg(method, payload))




class server(threading.Thread):
    def __init__(self, host, port):  
        print("Initializing WS Server") 
        threading.Thread.__init__(self)
        self.host = host
        self.port = port


    # Send to single client
    async def sendToClient(self, websocket, method, payload):
        await websocket.send(msg(method, payload))
    
    # Broadcast to all clients
    async def broadcast(self, method, payload):
        websockets.broadcast(v.connections, msg(method, payload))

    async def connectionhandler(self, websocket):
        connectionid = str(uuid.uuid4())

        try:
            # Register user
            user = User(websocket)

            # Broadcast the amount of connected users to all clients
            await self.broadcast('ONLINEUSERS', len(v.connections))
            
            # Require the new connection to authenticate
            await user.send('AUTH', False)

            # Parse messages from client
            async for raw in websocket:
                message = json.loads(raw)
                method = message['m']
                payload = message['p']

                if method == 'AUTH':
                    await user.send('AUTH', True)
                else:
                    await user.send('ERR', {'code': 1, 'desc': 'Unknown method'})
                    await self.broadcast('Something', payload)

        finally:
            # Unregister user
            user.remove()
            await self.broadcast('ONLINEUSERS', len(v.connections))
            

    async def startserver(self):
        async with websockets.serve(self.connectionhandler, self.host, self.port):
            await asyncio.Future()  # run forever

    def run(self): 
        asyncio.run(self.startserver())  

