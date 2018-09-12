#!/usr/bin/env bash


cat config.txt crontab_raspberry.txt > crontab.txt
crontab crontab.txt