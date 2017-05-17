#!/bin/bash

lists=(0 4 5 6 7 8 9 10 11 12 13)
for l in ${lists[@]} ; do
  while [ `ps -ef | grep "python3 main.py" | grep -v grep | wc -l` -gt 12 ] ; do sleep 1 ; done
  echo python3 main.py --list $l --type month --date 20170501
  python3 main.py --list $l --type month --date 20170501 &
done

while [ `ps -ef | grep "python3 main.py" | grep -v grep | wc -l` -ge 1 ] ; do sleep 1 ; done
echo "rm empty file"
for f in `ls data/zhaihehe/*/month/*.csv` ; do
  if [ `ls -l $f | awk '{ print $5 }'` -le 500 ] ; then echo `ls -l $f` ; fi
  if [ `ls -l $f | awk '{ print $5 }'` -le 500 ] ; then rm -f $f ; fi
done
