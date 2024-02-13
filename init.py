# Hi test bla

import sys
import pathlib
import threading
import mokkalib


#Custom modules
sys.path.insert(0, str(pathlib.Path(__file__).parent.resolve()) + '/lib')
import servers      # HTTP and Websocket Server
import handlers     # Handlers for Websocket Server
import database     # Database
import main         # Main program

# Initialize Mokkalib
mokkalib.init()
mokkalib.setEventHandler(handlers.mokkaEvent)

# Initialize Main Program Object
main.m = main.Main(database.DB(mokkalib.getOption('db_host'), mokkalib.getOption('db_port'), mokkalib.getOption('db_user'), mokkalib.getOption('db_password'), mokkalib.getOption('db_database')),
              servers.newHTTPServer(mokkalib.getOption('server_host'), mokkalib.getOption('server_port_http'), "www"),
              servers.newWebSocketServer(mokkalib.getOption('server_host'), mokkalib.getOption('server_port_websocket'), handlers.connectionhandler, handlers.messagehandler, handlers.disconnecthandler)
              )



