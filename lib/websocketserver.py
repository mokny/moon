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

class server(threading.Thread):
    def __init__(self, host, port):  
        print("Initializing WS Server") 
        threading.Thread.__init__(self)
        self.host = host
        self.port = port

    async def connectionhandler(self, websocket):
        connectionid = str(uuid.uuid4())

        try:
            # Register user
            v.users[connectionid] = {
                'connectionid': connectionid,
                'ip': websocket.remote_address[0],
                'socket': websocket,
                'data': {},
            }

            v.connections.add(websocket)

            # Broadcast the amount of connected users to all clients
            websockets.broadcast(v.connections, msg('ONLINEUSERS', len(v.connections)))
            
            # Require the new connection to authenticate
            await websocket.send(msg('AUTH', False))

            # Parse messages from client
            async for raw in websocket:
                message = json.loads(raw)
                method = message['m']
                payload = message['p']

                if method == 'AUTH':
                    await websocket.send(msg('AUTH', True))
                else:
                    await websocket.send(msg('ERR', {'code': 1, 'desc': 'Unknown method'}))
                    websockets.broadcast(v.connections, msg('NEW', False))
                    
        finally:
            # Unregister user
            del v.users[connectionid]
            v.connections.remove(websocket)
            websockets.broadcast(msg('DISC', False))
            #websockets.broadcast(USERS, users_event())

    async def startserver(self):
        async with websockets.serve(self.connectionhandler, self.host, self.port):
            await asyncio.Future()  # run forever

    def run(self): 
        asyncio.run(self.startserver())  

