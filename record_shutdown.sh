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
                mount /mnt
                rm /mnt/*.tar
                tar -cvf /mnt/$date.tar /var/log/.
                sync
                umount /mnt
                sync
                rm /tmp/shutdown
                /sbin/halt -p
        else
                echo "Button is $BUTTON, Not shutting down"
        fi
fi
