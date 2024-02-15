# Hi test bla

import sys
import pathlib
import mokkalib
import time
import signal

#Custom modules
sys.path.insert(0, str(pathlib.Path(__file__).parent.resolve()) + '/lib')
sys.path.insert(0, str(pathlib.Path(__file__).parent.resolve()) + '/custom')
import servers      # HTTP and Websocket Server
import handlers     # Handlers for Websocket Server
import database     # Database
import main         # Main program
import sys

def sigterm_handler(_signo, _stack_frame):
    print("Term received")
    main.m.webserver.kill()
    sys.exit(0)

signal.signal(signal.SIGTERM, sigterm_handler)


try:
    # Initialize Mokkalib
    mokkalib.init()
    mokkalib.setEventHandler(handlers.mokkaEvent)

    # Initialize Main Program Object
    main.m = main.Main(database.newDB('SQLITE','main.db'),
                servers.newWebServer(mokkalib.getOption('server_host'), mokkalib.getOption('server_port_http'), "www"),
                servers.newWebSocketServer(mokkalib.getOption('server_host'), mokkalib.getOption('server_port_websocket'), handlers.connectionhandler, handlers.messagehandler, handlers.disconnecthandler)
                )
    
    
    print(main.m.database.execute('DROP TABLE users'))
    print(main.m.database.execute('CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, password TEXT NOT NULL)'))
    print(main.m.database.execute("""INSERT INTO users (username, password) VALUES
        ('mokny', 'asd'),
        ('lala', 'asd'),
        ('beb', 'asd')"""))
    print(main.m.database.execute('SELECT * FROM users'))

    while True:
        time.sleep(1)
    
finally:
    print("Shutting down...")
    main.m.webserver.kill()
    print("Shutdown complete.")

