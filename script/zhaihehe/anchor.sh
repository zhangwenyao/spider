#!/bin/bash

file="data/zhaihehe/anchor-lists.txt"
if [ ! -f "${file}" ]; then
  echo error
  exit 1
fi

#lists=(0 4 5 6 7 8 9 10 11 12 13)
cat ${file} | while read line
do
  while [ `ps -ef | grep "python3 live.py" | grep -v grep | wc -l` -gt 12 ] ; do sleep 1 ; done
  echo python3 live.py --web zhaihehe --type anchor --date 20170423 --list 8 --range1 ${line} --range2 ${line}
  python3 live.py --web zhaihehe --type anchor --date 20170423 --list 8 --range1 ${line} --range2 ${line} &
done
