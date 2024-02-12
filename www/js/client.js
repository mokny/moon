var client;


class Client {
    
    constructor(serveraddr) {
        this.serveraddr = serveraddr;
        this.socket = false
        this.connected = false;
        this.reconnects = 0;
        this.maxreconnects = 10;
        this.connect()
    }

    connect() {
        if (this.connected) return;
        this.reconnects++;

        this.socket = new WebSocket(this.serveraddr)
        
        this.socket.onopen = ({ event }) => {
            this.reconnects = 0;
            this.connected = true;
        };
        
        this.socket.onmessage = ({ data }) => {
            this.parsemessage(data)
        };

        this.socket.onclose = ({ event }) => {
            this.disconnected();
        };

    }

    disconnected() {
        this.connected = false;
        if (this.reconnects < this.maxreconnects) {
            setTimeout(() => {
                this.connect();
            }, 1000);
        }
    }

    parsemessage(data) {
        console.log(data);
    }

    send(method, payload) {
        this.socket.send(JSON.stringify({ m: method, p: payload }));
    }    
}

function init() {
    client = new Client("ws://192.168.178.5:9002/")
}

window.addEventListener("DOMContentLoaded", () => {
    init();
}); 
