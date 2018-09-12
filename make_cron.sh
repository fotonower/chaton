#!/usr/bin/env bash

sudo pip install --upgrade fotonower
crontab -l > crontab.backup.`date "+%Y%m%d%H_%M"`
cat config.txt crontab_raspberry.txt > crontab.txt
crontab crontab.txt