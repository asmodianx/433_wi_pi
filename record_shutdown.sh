#!/bin/bash
BUTTON=`/usr/local/bin/button.py`
date=`date +%Y%m%d_%H%M`

if [ -f /tmp/shutdown ]; then
        echo "Already shutting down"
else
        touch /tmp/shutdown
        if [ $BUTTON = "1" ]; then
                service kismet stop
                service rtl_433 stop
                killall rtl_433
                killall kismet_server
                mount /mnt
                rm /mnt/*.tar
                tar -cvf /mnt/$date.tar /var/log/.
                sync
                umount /mnt
                sync
                #The Gps will take time to start up and get a fix while it does so everything will appear to be at kanza hall for a seckc meeting.
                echo "38.9130449,-94.6712426">/tmp/gps.txt
                rm /tmp/shutdown
                /sbin/halt -p
        else
                echo "Button is $BUTTON, Not shutting down"
        fi
fi
