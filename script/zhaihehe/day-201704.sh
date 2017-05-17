#!/bin/bash

dates=(20170401 20170402 20170403 20170404 20170405 20170406 20170407 20170408 20170409 \
  20170410 20170411 20170412 20170413 20170414 20170415 20170416 20170417 20170418 20170419 \
  20170420 20170421 20170422 20170423 20170424 20170425 20170426 20170427 20170428 20170429 \
  20170430)
lists=(0 4 5 6 7 8 9 10 11 12 13)
for d in ${dates[@]}; do
  for l in ${lists[@]} ; do
    while [ `ps -ef | grep "python3 main.py" | grep -v grep | wc -l` -gt 12 ] ; do sleep 1 ; done
    fn=data/zhaihehe/$l/day/$d.csv
    if [ -f $fn ] ; then
      if [ `ls -l $fn | awk '{ print $5 }'` -gt 500 ] ; then continue; fi
    fi
    echo python3 main.py --list $l --type day --date $d
    python3 main.py --list $l --type day --date $d &
  done
done

while [ `ps -ef | grep "python3 main.py" | grep -v grep | wc -l` -ge 1 ] ; do sleep 1 ; done
echo "rm empty file"
for f in `ls data/zhaihehe/*/day/*.csv` ; do
  if [ `ls -l $f | awk '{ print $5 }'` -le 500 ] ; then echo `ls -l $f` ; fi
  if [ `ls -l $f | awk '{ print $5 }'` -le 500 ] ; then rm -f $f ; fi
done
