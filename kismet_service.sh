#!/bin/bash

#***runs server then splices in gps information for each console log event.  
#***The kismet syslog plugin is nice but I cant splice in gps information like I do in rtl_433

/usr/bin/kismet_server|/usr/local/bin/gps_filter.sh|logger -t kismet
