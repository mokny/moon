import main 

# Mokkalib Handlers

def mokkaEvent(event):
    print(event)

# Websocket Handlers

async def connectionhandler(server, client):
    print("New connection from " + str(client.ip) + " Path: " + str(client.path) + ' ID: ' + str(client.id))
    await client.send('AUTH', False)
    await server.broadcast('ONLINEUSERS', len(server.connections))
    x = main.m.database.execute('SELECT * FROM users')
    await client.send('test', x[0]['username'])
    print(x[0]['username'])    


async def messagehandler(server, client, method, payload):
    print("msghandler here")
    await client.send('RECV', str(client.secondsConnected()) + ' ' + client.path)


async def disconnecthandler(server, client):
    print("Client " + str(client.id) + " disconnected.")
    await server.broadcast('ONLINEUSERS', len(server.connections))
