#!/bin/bash

lists=(0 4 5 6 7 8 9 10 11 12 13)
for l in ${lists[@]} ; do
  while [ `ps -ef | grep "python3 main.py" | grep -v grep | wc -l` -gt 12 ] ; do sleep 1 ; done
  echo python3 main.py --list $l --type month --date 20170501
  python3 main.py --list $l --type month --date 20170501 &
done
