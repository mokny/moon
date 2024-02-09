# Hi test bla

import sys
import pathlib
import threading
import mokkalib
mokkalib.init()

#Custom modules
sys.path.insert(0, str(pathlib.Path(__file__).parent.resolve()) + '/lib')

import vars as v
import httpserver
import websocketserver

workspace = mokkalib.getWorkspace()


def mokkaEvent(event):
    print(event)

mokkalib.setEventHandler(mokkaEvent)

# Start Webserver
httpserver.server("", 9000, "www").start()

# Start Websocketserver
websocketserver.server("192.168.178.5", 9002).start()

mokkalib.triggerGlobalEvent('TANKS ONLINE')

