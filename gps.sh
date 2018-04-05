#!/bin/bash
gpstmp=`mktemp`
GPS=`gpspipe -w|grep -m 1 "TPV"|cut -d , -f 6,7`
lat=`echo $GPS|cut -d , -f 1 |cut -d : -f2`
lon=`echo $GPS|cut -d , -f 2 |cut -d : -f2`
echo $lat,$lon > $gpstmp
chmod 644 $gpstmp
mv $gpstmp /tmp/gps.txt 
