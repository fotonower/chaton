#!/bin/bash
for pid in $(pidof -x sh /home/pi/workarea/git/raspberrypi/myscript.sh); do
    echo $$
    echo $pid
    echo $(pidof -x sh /home/pi/workarea/git/raspberrypi/myscript.sh)
    if [ $pid != $$ ]; then
	echo 'script allready launched'
        exit 1
    fi
done

pause=""
if [ -n $1 ]
then
    pause=" -p $1"
fi

if [ -n $2 ]
then
    pause=$pause" -e $2"
fi

echo $pause

echo "launching script"
python /home/pi/workarea/git/raspberrypi/get_pic_by_seconds.py$pause
echo "after launch"
