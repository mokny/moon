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

