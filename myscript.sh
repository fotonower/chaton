#!/bin/bash
for pid in $(pidof -x myscript.sh); do
    if [ $pid != $$ ]; then
	echo 'script allready launched'
        exit 1
    fi
done

pause=""
if [-n $1]
then
    pause=" -p $1"
fi

if [-n $2]
then
echo "launching script"
fi

python /home/pi/workarea/git/raspberrypi/get_pic_by_seconds.py$pause
echo "after launch"
