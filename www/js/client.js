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
        this.onLatencyChangedHandler = false;
        this.pingInterval = 10000;
        this.latency = 0;
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

    setOnLatencyChangedHandler(func) {
        this.onLatencyChangedHandler = func;
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
            this.ping();
        };
        
        this.socket.onmessage = ({ data }) => {
            if (this.onMessageHandler) {
                try {
                    var msg = JSON.parse(data);
                    if (msg['m'] == 'XPONG') {
                        this.latency = performance.now() - msg['p'];
                        if (this.onLatencyChangedHandler) {
                            this.onLatencyChangedHandler('CLIENT', this.latency);
                        }
                    } else if (msg['m'] == 'XPING') {
                        this.send('XPONG', msg['p']);
                    } else if (msg['m'] == 'XLAT') {
                        this.latency = msg['p'];
                        this.onLatencyChangedHandler('SERVER', this.latency);
                    } else {
                        this.onMessageHandler(msg['m'], msg['p']);
                    }
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

    ping() {
        if (this.pingInterval > 0) {
            this.send("XPING", performance.now());
            setTimeout(() => {
                this.ping();
            }, this.pingInterval);
        }
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

