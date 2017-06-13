#!/bin/bash

file="infiles/zhaihehe-weeks-list.txt"
if [ ! -f "${file}" ]; then
  exit 1
fi

lists=(0 4 5 6 7 8 9 10 11 12 13)
cat ${file} | while read line
do
  for l in ${lists[@]} ; do
    while [ `ps -ef | grep "python3 main.py --web zhaihehe" | grep -v grep | wc -l` -gt 12 ] ; do sleep 1 ; done
    echo python3 main.py --web zhaihehe --type week --list $l ${line}
    python3 main.py --web zhaihehe --type week --list $l ${line} &
  done
done

while [ `ps -ef | grep "python3 main.py --web zhaihehe" | grep -v grep | wc -l` -ge 1 ] ; do sleep 1 ; done
echo "rm empty file"
for f in `ls data/zhaihehe/*/week/*.csv` ; do
  if [ `ls -l $f | awk '{ print $5 }'` -le 500 ] ; then echo `ls -l $f` ; fi
  if [ `ls -l $f | awk '{ print $5 }'` -le 500 ] ; then rm -f $f ; fi
done
