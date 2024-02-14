# Hi test bla

import sys
import pathlib
import threading
import mokkalib
import time
import signal

#Custom modules
sys.path.insert(0, str(pathlib.Path(__file__).parent.resolve()) + '/lib')
import servers      # HTTP and Websocket Server
import handlers     # Handlers for Websocket Server
import database     # Database
import main         # Main program
import sys

def sigterm_handler(_signo, _stack_frame):
    print("Term received")
    main.m.httpserver.kill()
    sys.exit(0)

signal.signal(signal.SIGTERM, sigterm_handler)


try:
    # Initialize Mokkalib
    mokkalib.init()
    mokkalib.setEventHandler(handlers.mokkaEvent)

    # Initialize Main Program Object
    main.m = main.Main(database.DB(mokkalib.getOption('db_host'), mokkalib.getOption('db_port'), mokkalib.getOption('db_user'), mokkalib.getOption('db_password'), mokkalib.getOption('db_database')),
                servers.newWebServer(mokkalib.getOption('server_host'), mokkalib.getOption('server_port_http'), "www"),
                servers.newWebSocketServer(mokkalib.getOption('server_host'), mokkalib.getOption('server_port_websocket'), handlers.connectionhandler, handlers.messagehandler, handlers.disconnecthandler)
                )
    while True:
        time.sleep(1)
    
finally:
    print("Shutting down...")
    main.m.webserver.kill()
    print("Shutdown complete.")

