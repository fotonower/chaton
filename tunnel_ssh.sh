#!/usr/bin/env bash

PORT_DEFAULT=19999
if [ -z "$1" ]
then
	PORT=$PORT_DEFAULT
else
	PORT=$1
fi
val=`ps -aef | grep charlot.fotonower.com | grep $PORT | wc -l`

if [ "$val" -lt 1 ]; then
    echo "Need to relaunch ssh tunnelling ! val : "$val
    ssh-add -l &>/dev/null
    echo "testing ssh_add"
    if [ "$?" == 2 ]; then
        test -r ~/.ssh-agent && \
        eval "$(<~/.ssh-agent)" >/dev/null

        ssh-add -l &>/dev/null
        if [ "$?" == 2 ]; then
            (umask 066; ssh-agent > ~/.ssh-agent)
            eval "$(<~/.ssh-agent)" >/dev/null
            ssh-add
        fi
    fi
    nohup ssh -N -i /home/pi/.ssh/pi3_64_160618_rsa -R $PORT:localhost:22 fotonower@charlot.fotonower.com &
    echo "Ssh tunnelling launched !"
else
    echo " val : $val : ssh tunnelling is running"
fi
