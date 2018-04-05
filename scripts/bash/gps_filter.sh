#!/bin/bash
while read -r line
do
        GPS=`cat /tmp/gps.txt`
        output="$GPS $line"
        echo $output
done < "${1:-/dev/stdin}"
