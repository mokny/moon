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
import database

workspace = mokkalib.getWorkspace()


def mokkaEvent(event):
    print(event)

mokkalib.setEventHandler(mokkaEvent)

# Init Database
v.db = database.DB('localhost', 3306, 'spc', 'password', 'spc')

# Start Webserver
v.httpserver = servers.newHTTPServer("", 9000, "www")

# Start Websocketserver
v.websocketserver = servers.newWebSocketServer("192.168.178.5", 9002, handlers.connectionhandler, handlers.messagehandler, handlers.disconnecthandler)

mokkalib.triggerGlobalEvent('TANKS ONLINE')

