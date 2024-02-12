async def connectionhandler(server, client):
    print("Conhandler her")
    await client.send('AUTH', False)
    await server.broadcast('ONLINEUSERS', len(server.connections))


async def messagehandler(server, client, method, payload):
    print("msghandler here")
    await client.send('RECV',payload)


async def disconnecthandler(server, client):
    print("DisConhandler her")
    await server.broadcast('ONLINEUSERS', len(server.connections))
