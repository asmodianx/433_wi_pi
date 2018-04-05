#!/bin/bash
/usr/local/bin/rtl_433 -F json -G|/usr/local/bin/gps_filter.sh|logger -t rtl_433
