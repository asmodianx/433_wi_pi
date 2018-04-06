#!/usr/bin/env python

## *** UDP SYSLOG Server that appends GPSD location ***
# Its hacked together from several different sources



#import libraries
import logging
import os
import time
import threading
import SocketServer
#from logging.handlers import SysLogHandler
from gps import *
from time import *

 
gpsd = None #seting the global variable

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
 


#syslog udp handler - opens configured port and updates data object with incomming syslog message and appends gpsd lat and long and writes to log file

class SyslogUDPHandler(SocketServer.BaseRequestHandler):
        def handle(self):
                data = bytes.decode(self.request[0].strip()) + "(" +str(gpsd.fix.latitude) + "," + str(gpsd.fix.longitude) + ")"
                socket = self.request[1]
                #print( "%s : " % self.client_address[0], str(data)) # not needed
                logging.info(str(data))
         

#set configuration
LOG_FILE = '/var/log/gpsd_433wipi_logs.log'
HOST, PORT = "127.0.0.1", 2514

global gpsp

os.system('clear') #clear the terminal (optional)

#configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s', datefmt='', filename=LOG_FILE, filemode='a') #for writing to local file

# *** possibility: a syslog filter ***
# rather than dumping everything forwarded to this service to a file we can fire it right back to to the local syslog server and route the 
# log that way.  though this leads to duplication if we are not careful
# ***
#logging.handlers.SysLogHandler(address=('localhost', 514),facility=LOG_USER, socktype=socket.SOCK_DGRAM) #open syslog connection back to main server with gps encrusted input
#syslogger = logging.getLogger()
#logging.warn("Hello world")

if __name__ == "__main__":
        try:
                gpsp = GpsPoller() # create the thread
                gpsp.start() # start it up
                server = SocketServer.UDPServer((HOST,PORT), SyslogUDPHandler)
                server.serve_forever(poll_interval=0.5)
        except (IOError, SystemExit):
                raise
        except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
                print "\nKilling Thread..."
                gpsp.running = False
                gpsp.join() # wait for the thread to finish what it's doing
                sys.exit("Crtl+C Pressed. Shutting down.")
