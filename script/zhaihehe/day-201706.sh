#!/bin/bash

#dates=(20170601 20170602 20170603 20170604 20170605 20170606 20170607 20170608 20170609 \
  #20170610 20170611 20170612 20170613 20170614 20170615 20170616 20170617 20170618 20170619 \
  #20170620 20170621 20170622 20170623 20170624 20170625 20170626 20170627 20170628 20170629 \
  #20170630 20170631)
dates=(20170601 20170602 20170603 20170604 20170605 20170606 20170607 20170608 20170609 \
  20170610 20170611)
lists=(0 4 5 6 7 8 9 10 11 12 13)
for d in ${dates[@]}; do
  for l in ${lists[@]} ; do
    while [ `ps -ef | grep "python3 main.py --web zhaihehe" | grep -v grep | wc -l` -gt 12 ] ; do sleep 1 ; done
    fn=data/zhaihehe/$l/day/$d.csv
    if [ -f $fn ] ; then
      if [ `ls -l $fn | awk '{ print $5 }'` -gt 500 ] ; then continue; fi
    fi
    echo python3 main.py --web zhaihehe --list $l --type day --date $d
    python3 main.py --list $l --type day --date $d &
  done
done

while [ `ps -ef | grep "python3 main.py --zhaihehe" | grep -v grep | wc -l` -ge 1 ] ; do sleep 1 ; done
echo "rm empty file"
for f in `ls data/zhaihehe/*/day/*.csv` ; do
  if [ `ls -l $f | awk '{ print $5 }'` -le 500 ] ; then echo `ls -l $f` ; fi
  if [ `ls -l $f | awk '{ print $5 }'` -le 500 ] ; then rm -f $f ; fi
done
