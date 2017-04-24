#!/bin/bash

dates=(20170101 20170201 20170301)
lists=(0 4 5 6 7 8 9 10 11 12 13)
for d in ${dates[@]} ; do
  for l in ${lists[@]} ; do
    while [ `ps -ef | grep "python3 live.py" | grep -v grep | wc -l` -gt 12 ] ; do sleep 1 ; done
    echo python3 live.py --list $l --type month --date ${d}
    python3 live.py --list $l --type month --date ${d} &
  done
done
