#!/bin/bash

appIds=(189)
lists=(1 2 3)
for i in ${appIds[@]} ; do
  for l in ${lists[@]} ; do
    echo python3 live.py --web talkingdata --type app --listname $i --list $l --dateType w --date 20150105 --date2 20171231
    python3 live.py --web talkingdata --type app --listname $i --list $l --dateType w --date 20150105 --date2 20171231
  done
done
