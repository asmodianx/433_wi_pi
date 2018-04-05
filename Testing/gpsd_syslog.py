#!/usr/bin/env python

## *** UDP SYSLOG Server that appends GPSD location ***


import os
from gps import *
from time import *
import time
import threading
import logging
import SocketServer

gpsd = None #seting the global variable

os.system('clear') #clear the terminal (optional)

LOG_FILE = 'gps_433wipi_logs.log'
HOST, PORT = "0.0.0.0", 2514


class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true

  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer

logging.basicConfig(level=logging.INFO, format='%(message)s', datefmt='', filename=LOG_FILE, filemode='a')

class SyslogUDPHandler(SocketServer.BaseRequestHandler):

	def handle(self):
		data = bytes.decode(self.request[0].strip()) + str(gpsd.fix.longitude) + "," + str(gpsd.fix.latitude) + " "
		socket = self.request[1]
		print( "%s : " % self.client_address[0], str(data))
		logging.info(str(data))

if __name__ == "__main__":
	gpsp = GpsPoller()
	gpsp.start()
	try:
		server = SocketServer.UDPServer((HOST,PORT), SyslogUDPHandler)
		server.serve_forever(poll_interval=0.5)
	except (IOError, SystemExit):
		raise
	except KeyboardInterrupt:
		print ("Crtl+C Pressed. Shutting down.")
