# Hi test bla

import sys
import pathlib
import threading
import mokkalib

mokkalib.init()

#Custom modules
sys.path.insert(0, str(pathlib.Path(__file__).parent.resolve()) + '/lib')

import vars as v
import servers
import handlers

workspace = mokkalib.getWorkspace()


def mokkaEvent(event):
    print(event)

mokkalib.setEventHandler(mokkaEvent)

# Start Webserver
httpserver = servers.newHTTPServer("", 9000, "www")

# Start Websocketserver
websocketserver = servers.newWebSocketServer("192.168.178.5", 9002, handlers.connectionhandler, handlers.messagehandler, handlers.disconnecthandler)

mokkalib.triggerGlobalEvent('TANKS ONLINE')

