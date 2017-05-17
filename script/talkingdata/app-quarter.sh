#!/bin/bash

appIds=(189)
lists=(1 2 3)
for i in ${appIds[@]} ; do
  for l in ${lists[@]} ; do
    while [ `ps -ef | grep "python3 main.py" | grep -v grep | wc -l` -gt 12 ] ; do sleep 1 ; done
    echo python3 main.py --web talkingdata --type app --listname $i --list $l --dateType q --date 20160101 --date2 20171231
    python3 main.py --web talkingdata --type app --listname $i --list $l --dateType q --date 20160101 --date2 20171231 &
  done
done
