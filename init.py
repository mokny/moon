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
v.db = database.DB(mokkalib.getOption('db_host'), mokkalib.getOption('db_port'), mokkalib.getOption('db_user'), mokkalib.getOption('db_password'), mokkalib.getOption('db_database'))

# Start Webserver
v.httpserver = servers.newHTTPServer(mokkalib.getOption('server_host'), mokkalib.getOption('server_port_http'), "www")

# Start Websocketserver
v.websocketserver = servers.newWebSocketServer(mokkalib.getOption('server_host'), mokkalib.getOption('server_port_websocket'), handlers.connectionhandler, handlers.messagehandler, handlers.disconnecthandler)

mokkalib.triggerGlobalEvent('TANKS ONLINE')

