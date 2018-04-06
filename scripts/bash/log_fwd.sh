#!/bin/bash
#for seckc logging demo

# the file generated is already in syslog format so using syslog or logger to send it would be counter productive and add junk to it.
# modding the gpsd_syslog script to send traffic would be a better option as rather than writing a log file we can fire it right back
# to rsyslog and make use of its routing and processing capabilities.

tail -f /var/log/gpsd_433wipi_logs.log|nc -u 192.168.142.234 514
