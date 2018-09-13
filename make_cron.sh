#!/usr/bin/env bash

echo "updating fotonower package"
sudo pip install --upgrade fotonower
echo "checking sqlite"
echo "select day_taken_at as d, substr(hour_taken_at, 0, 3) as h, count(*) from mra_photos group by d, h;" | sqlite3 /home/pi/.fotonower_config/sqlite.db
if [[ "$?" -ne 0 ]];then
    echo "installing sqlite3"
    sudo apt-get install sqlite3
    sqlite3 ~/.fotonower_config/sqlite.db < ~/workarea/git/raspberrypi/raspberry_camera/sqlite/mtr_raspberry.sql
fi
echo "backuping current crontab"
crontab -l > crontab.backup.`date "+%Y%m%d%H_%M"`
echo "creating new crontab file with config.txt"
cat config.txt crontab_raspberry.txt > crontab.txt
echo "you need now to source crontab with crontab crontab.txt"

#crontab crontab.txt