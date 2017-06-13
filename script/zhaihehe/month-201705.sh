#!/bin/bash

lists=(0 4 5 6 7 8 9 10 11 12 13)
for l in ${lists[@]} ; do
  fn=data/zhaihehe/$l/month/20170501-20170531.csv
  if [ -f $fn ] ; then
    if [ `ls -l $fn | awk '{ print $5 }'` -gt 500 ] ; then continue; fi
  fi
  while [ `ps -ef | grep "python3 main.py --web zhaihehe" | grep -v grep | wc -l` -gt 12 ] ; do sleep 1 ; done
  echo python3 main.py --web zhaihehe --list $l --type month --date 20170501
  python3 main.py --web zhaihehe --list $l --type month --date 20170501 &
done

while [ `ps -ef | grep "python3 main.py --web zhaihehe" | grep -v grep | wc -l` -ge 1 ] ; do sleep 1 ; done
echo "rm empty file"
for f in `ls data/zhaihehe/*/month/*.csv` ; do
  if [ `ls -l $f | awk '{ print $5 }'` -le 500 ] ; then echo `ls -l $f` ; fi
  if [ `ls -l $f | awk '{ print $5 }'` -le 500 ] ; then rm -f $f ; fi
done
