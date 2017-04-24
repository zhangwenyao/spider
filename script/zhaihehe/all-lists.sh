#!/bin/bash

if [ $(($#%2)) -eq 1 ] ; then
  echo "usage : $0 [-d 20170101] [-2 20170203] [-t {day,week,month,other}]"
  exit 1
fi

lists=(0 4 5 6 7 8 9 10 11 12 13)
for l in ${lists[@]} ; do
  while [ `ps -ef | grep "python3 live.py" | grep -v grep | wc -l` -gt 12 ] ; do sleep 1 ; done
  echo python3 live.py --list $l $@ &
  python3 live.py --list $l $@ &
done

