#!/bin/bash
BUTTON=`/usr/local/bin/button.py`
if [ -f /tmp/shutdown ]; then
        echo "Already shutting down"
else
        touch /tmp/shutdown
        if [ $BUTTON = "1" ]; then
                mount /mnt
                rm /mnt/*.tgz
                /root/logs.sh
                sync
                umount /mnt
                sync
                rm /tmp/shutdown
                halt -p
        else
                echo "Button is $BUTTON, Not shutting down"
        fi
fi
