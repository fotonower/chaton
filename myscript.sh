#!/bin/bash
for pid in $(pidof -x myscript.sh); do
    if [ $pid != $$ ]; then
	echo 'script allready launched'
        exit 1
    fi
done
echo "launching script"
python /home/pi/workarea/git/raspberrypi/get_pic_by_seconds.py
echo "after launch"
