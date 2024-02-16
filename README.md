# Webserver and Websocket Framework

## Installation
```
mokka workspace create framework
mokka install framework /path
```
Now pick a project path (directory MUST NOT exist) and tell the framework to initialize it
```
mokka run framework framework setup </my/absolute/project/path>
mokka kill framework framework
```

Now configure the framework:
```
mokka setopt framework framework server_host <YourIPorHostname>
mokka setopt framework framework server_port_http <YourWebsitePort>
mokka setopt framework framework server_port_websocket <YourWebsocketPort>
```


Now run the framework:
```
mokka run framework framework
```

## Getting started
You defined a project directory in `</my/absolute/project/path>`. Go to that path and you will find a file and a folder. The file `framework_init.py` is the starting point for your project. It contains all handlers. Inside the `www` folder you will find an example html file from where to start.

## HTML coding (The Client-Side)
Start with the `index.html` inside the `www` folder. Basically you can use a complete custom HTML framework, as long as you load the client script. You need this in the header of your html file:
```HTML
<script src="framework_client" lang="JavaScript"></script>
```
Now your client is ready for configuration and connecting:
```JS
        function onConnect(event) {
            console.log("Connected");
        }

        function onDisconnect(event) {
            console.log("Disconnected");
        }

        function onReConnect(cnt) {
            console.log("Reconnecting...Try #" + cnt);
        }

        function onReConnectFailed() {
            console.log("Reconnect failed. No more retries.");
        }

        function onLatencyChanged(measuredby, latency) {
            console.log('Latency measured by '+ measuredby + ': ' + latency + 'ms');
        }

        function onMessage(method, payload) {
            console.log("Message");
            console.log(method + ' ' +  payload);
        }


        window.addEventListener("DOMContentLoaded", () => {
            WSSClient.setMaxReconnects(10);
            WSSClient.setReconnectDelay(2000);
            WSSClient.setOnConnectHandler(onConnect);
            WSSClient.setOnDisconnectHandler(onDisconnect);
            WSSClient.setOnMessageHandler(onMessage);
            WSSClient.setOnReconnectHandler(onReConnect);
            WSSClient.setOnReconnectFailedHandler(onReConnectFailed);
            WSSClient.setOnLatencyChangedHandler(onLatencyChanged);
            WSSClient.connect();            
        });  
```
Sending a message to the server works like this:
```JS
WSSClient.send('MYMETHOD','somepayload')
```


## Python coding (The Server-Side)
The file `framework_init.py` is your starting point. The minimum you need is this:
```python
class Framework():
    
    def __init__(self):
        self.main = False

    def start(self, main):
        self.main = main
    
    # Event handler for events from Mokka. 
    def mokkaEvent(self, event):
        pass

    # Gets called when a new websocket connection was established
    async def wsConnectionHandler(self, server, client):
        pass

    # Gets called when a new message was received via websockets
    async def wsMessageHandler(self, server, client, method, payload):
        pass

    # Gets called when a client disconnects
    async def wsDisconnectHandler(self, server, client):
        pass
```

### Sending Data to Clients via websockets
On every handler event, the client object gets passed to the handler. The easiest way to reply is this.
```python
await client.send('MYMETHOD', False)
```
The first parameter is a method string, and the second one is the payload, that can be any kind of datatype.

But you may also access a dictionary of all connected clients, that is stored in `self.main.websocketserver.clients`:

```python
print(self.main.websocketserver.clients)
```

To broadcast a message to all connected clients use:
```python
await self.main.websocketserver.broadcast('ONLINEUSERS', len(server.connections))
```

### Accessing the Database
By default a SQLite Database is created. To simply execute a statement use:
```python
self.main.database.execute('CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, password TEXT NOT NULL)')
```

To retrieve data use:
```python
result = self.main.database.execute('SELECT * FROM users')
print(result)
```
The result is always returned as a multi dimensional array with a dict for each returned row.
Example:
```python
result = self.main.database.execute('SELECT * FROM users')
print(result[0]['username'])    
```
