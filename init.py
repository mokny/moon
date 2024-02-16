# Hi test bla

import sys
import pathlib
import mokkalib
import time
import signal

mokkalib.init()

#Custom modules
sys.path.insert(0, str(pathlib.Path(__file__).parent.resolve()) + '/lib')

#Project root
sys.path.insert(0, mokkalib.getOption('root'))

import servers      # HTTP and Websocket Server
import database     # Database
import main         # Main program

def sigterm_handler(_signo, _stack_frame):
    print("Term received")
    main.m.webserver.kill()
    sys.exit(0)

signal.signal(signal.SIGTERM, sigterm_handler)


try:
    import framework_init

    main.f = framework_init.Framework()
    mokkalib.setEventHandler(main.f.mokkaEvent)

    main.m = main.Main(database.newDB('SQLITE',mokkalib.getOption('db_filename')),
                servers.newWebServer(mokkalib.getOption('server_host'), mokkalib.getOption('server_port_http'), mokkalib.getOption('httpdocs')),
                servers.newWebSocketServer(mokkalib.getOption('server_host'), mokkalib.getOption('server_port_websocket'), main.f.wsConnectionHandler, main.f.wsMessageHandler, main.f.wsDisconnectHandler)
                )
    
    main.f.start(main.m)

    while True:
        time.sleep(1)
    
finally:
    print("Shutting down...")
    main.m.webserver.kill()
    print("Shutdown complete.")

