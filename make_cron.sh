#!/usr/bin/env bash

echo "updating fotonower package"
sudo pip install --upgrade fotonower
echo "backuping current crontab"
crontab -l > crontab.backup.`date "+%Y%m%d%H_%M"`
echo "creating new crontab file with config.txt"
cat config.txt crontab_raspberry.txt > crontab.txt
echo "you need now to source crontab with crontab crontab.txt"
#crontab crontab.txt