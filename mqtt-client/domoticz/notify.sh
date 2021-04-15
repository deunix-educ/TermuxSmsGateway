#!/usr/bin/bash
/usr/bin/python3 /home/domosquitto/domoticz/scripts/smsquitto.py \
    --method=notify --host=$1 --port=$2 --user=$3 --password=$4 --apikey=$5 --text="$6" $7 \
    > /dev/null 2>&1 &