#!/bin/bash

dates=(20160101 20160201 20160301 20160401 20160501 20160601 20160701 20160801 20160901 20161001 20161101 20161201 \
  20170101 20170201 20170301)
appIds=(189)
for d in ${dates[@]}; do
  for l in ${appIds[@]} ; do
    echo python3 live.py --web talkingdata --type app --listname $l --list 4 --date $d
    python3 live.py --web talkingdata --type app --listname $l --list 4 --date $d
  done
done
