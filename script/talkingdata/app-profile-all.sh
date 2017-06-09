#!/bin/bash

dates=(20160101 20160201 20160301 20160401 20160501 20160601 20160701 20160801 20160901 20161001 20161101 20161201 \
  20170101 20170201 20170301 20170401 20170501 20170601 20170701 20170801 20170901 20171001 20171101 20171201)
appIds=(189)
for d in ${dates[@]}; do
  for appId in ${appIds[@]} ; do
    while [ `ps -ef | grep "python3 main.py" | grep -v grep | wc -l` -gt 12 ] ; do sleep 1 ; done
    cmd="python3 main.py --web talkingdata --type app --listname $appId --list 4 --date $d &"
    echo $cmd
    echo $cmd | sh
  done
done
