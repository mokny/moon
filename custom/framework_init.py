class Framework():
    
    def __init__(self):
        self.main = False

    def start(self, main):
        self.main = main
        self.main.webserver.setscriptfunction('test', self.test)

        print(self.main.database.execute('DROP TABLE users'))
        print(self.main.database.execute('CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, password TEXT NOT NULL)'))
        print(self.main.database.execute("""INSERT INTO users (username, password) VALUES
            ('mokny', 'asd'),
            ('lala', 'asd'),
            ('beb', 'asd')"""))
        print(self.main.database.execute('SELECT * FROM users'))
    
    def test(self, params):
        return 'yop' + str(params)     
      
    # Mokkalib Handlers
    
    def mokkaEvent(self, event):
        print(event)

    # Websocket Handlers

    async def wsConnectionHandler(self, server, client):
        print("New connection from " + str(client.ip) + " Path: " + str(client.path) + ' ID: ' + str(client.id))
        print("PARTY")
        await client.send('PARTY', False)
        await client.send('AUTH', False)
        await server.broadcast('ONLINEUSERS', len(server.connections))
        x = self.main.database.execute('SELECT * FROM users')
        await client.send('test', x[0]['username'])
        print(x[0]['username'])    


    async def wsMessageHandler(self, server, client, method, payload):
        print("msghandler here")
        await client.send('RECV', str(client.secondsConnected()) + ' ' + client.path)


    async def wsDisconnectHandler(self, server, client):
        print("Client " + str(client.id) + " disconnected.")
        await server.broadcast('ONLINEUSERS', len(server.connections))