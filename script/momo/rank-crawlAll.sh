#!/bin/bash
echo `date` $0
config="config/momo-rank.json"
cd /home/yao/files/git/spider
python3 main.py -c $config --web momo --type rank --rankType star_hour      > /dev/null 2>&1
python3 main.py -c $config --web momo --type rank --rankType star_potential > /dev/null 2>&1
python3 main.py -c $config --web momo --type rank --rankType star_day       > /dev/null 2>&1
python3 main.py -c $config --web momo --type rank --rankType star_week      > /dev/null 2>&1
python3 main.py -c $config --web momo --type rank --rankType user_day       > /dev/null 2>&1
python3 main.py -c $config --web momo --type rank --rankType user_week      > /dev/null 2>&1
