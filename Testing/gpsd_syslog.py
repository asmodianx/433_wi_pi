#!/usr/bin/env python
## *** UDP SYSLOG Server that appends GPSD location ***

#import libraries
import os
from gps import *
from time import *
import time
import threading
import logging
import SocketServer

#GPS poller - starts thread that starts wild loop updating next gps value in gpsd object
class GpsPoller(threading.Thread):
        def __init__(self):
                threading.Thread.__init__(self)

        global gpsd #bring it in scope
        gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
        gpsd.current_value = None
        gpsd.running = True #setting the thread running to true

        def run(self):
                global gpsd
                while gpsd.running:
                        gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer

#syslog udp handler - opens configured port and updates data object with incomming syslog message and appends gpsd lat and long and writes to log file

class SyslogUDPHandler(SocketServer.BaseRequestHandler):
        def handle(self):
                data = bytes.decode(self.request[0].strip()) + " " +str(gpsd.fix.latitude) + "," + str(gpsd.fix.longitude)
                socket = self.request[1]
                print( "%s : " % self.client_address[0], str(data))
                logging.info(str(data))

#set configuration
LOG_FILE = 'gps_433wipi_logs.log'
HOST, PORT = "127.0.0.1", 2514

#start gps poller in thread
gpsd = None #seting the global variable
gpsd = GpsPoller()
gpsd.start()

os.system('clear') #clear the terminal (optional)

#configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s', datefmt='', filename=LOG_FILE, filemode='a')

if __name__ == "__main__":
        try:
                server = SocketServer.UDPServer((HOST,PORT), SyslogUDPHandler)
                server.serve_forever(poll_interval=0.5)
        except (IOError, SystemExit):
                raise
        except KeyboardInterrupt:
                print ("Crtl+C Pressed. Shutting down.")
