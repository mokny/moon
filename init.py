# Hi test bla

import sys
import pathlib
import threading
import mokkalib
mokkalib.init()

#Custom modules
sys.path.insert(0, str(pathlib.Path(__file__).parent.resolve()) + '/lib')

import httpserver
import websocketserver

httpserver.server("", 9000, "www").start()
websocketserver.server("", 9000, "www").start()

def mokkaEvent(event):
    print(event)

mokkalib.setEventHandler(mokkaEvent)
mokkalib.triggerGlobalEvent('TANKS ONLINE')
workspace = mokkalib.getWorkspace()