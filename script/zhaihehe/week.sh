#!/bin/bash

file="infiles/zhaihehe-weeks-list.txt"
if [ ! -f "${file}" ]; then
  exit 1
fi

lists=(0 4 5 6 7 8 9 10 11 12 13)
cat ${file} | while read line
do
  for l in ${lists[@]} ; do
    while [ `ps -ef | grep "python3 main.py" | grep -v grep | wc -l` -gt 12 ] ; do sleep 1 ; done
    echo python3 main.py --type week --list $l ${line}
    python3 main.py --type week --list $l ${line} &
  done
done
