#!/bin/bash
for pid in $(pidof -x myscript.sh); do
    if [ $pid != $$ ]; then
        exit 1
    fi
done
python get_pic_by_seconds.py
