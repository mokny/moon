class Client {
    
    constructor(serveraddr) {
        this.serveraddr = serveraddr;
        this.socket = false
        this.connected = false;
        this.reconnects = 0;
        this.maxreconnects = 10;
        this.reconnectdelay = 1000;
        this.onConnectHandler = false;
        this.onMessageHandler = false;
        this.onDisconnectHandler = false;
        this.onReconnectHandler = false;
        this.onReconnectFailedHandler = false;
    }

    setMaxReconnects(value) {
        this.maxreconnects = value;
    }

    setReconnectDelay(value) {
        this.reconnectdelay = value;
    }

    setOnMessageHandler(func) {
        this.onMessageHandler = func;
    }

    setOnConnectHandler(func) {
        this.onConnectHandler = func;
    }

    setOnDisconnectHandler(func) {
        this.onDisconnectHandler = func;
    }

    setOnReconnectHandler(func) {
        this.onReconnectHandler = func;
    }

    setOnReconnectFailedHandler(func) {
        this.onReconnectFailedHandler = func;
    }

    connect() {
        if (this.connected) return;
        this.reconnects++;

        this.socket = new WebSocket(this.serveraddr)
        
        this.socket.onopen = ({ event }) => {
            this.reconnects = 0;
            this.connected = true;
            if (this.onConnectHandler) {
                this.onConnectHandler(event);
            }
        };
        
        this.socket.onmessage = ({ data }) => {
            if (this.onMessageHandler) {
                try {
                    var msg = JSON.parse(data);
                    this.onMessageHandler(msg['m'], msg['p']);
                } catch(error) {
                    console.log(error);
                }
            }
        };

        this.socket.onclose = ({ event }) => {
            if (this.onDisconnectHandler) {
                this.onDisconnectHandler(event);
            }
            this.disconnected();
        };

    }

    disconnected() {
        this.connected = false;
        if (this.reconnects < this.maxreconnects) {
            if (this.onReconnectHandler) {
                this.onReconnectHandler(this.reconnects);
            }
            setTimeout(() => {
                this.connect();
            }, this.reconnectdelay);
        } else {
            if (this.onReconnectFailedHandler) {
                this.onReconnectFailedHandler();
            }
        }
    }

    parsemessage(data) {
        console.log(data);
    }

    send(method, payload) {
        this.socket.send(JSON.stringify({ m: method, p: payload }));
    }    
}

