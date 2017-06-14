#!/bin/bash


# cd to spider project
#   get absolute path
dir0=$(dirname $0)
if [ "${dir0:0:1}"x != "/"x ]; then
  dir0=`pwd`/$dir0
fi
cd $dir0
dir0=`pwd`
#   cd ../..
dir0=$(dirname $dir0)
dir0=$(dirname $dir0)
cd $dir0


dates=(20170501 20170502 20170503 20170504 20170505 20170506 20170507 20170508 20170509 \
  20170510 20170511 20170512 20170513 20170514 20170515 20170516 20170517 20170518 20170519 \
  20170520 20170521 20170522 20170523 20170524 20170525 20170526 20170527 20170528 20170529 \
  20170530 20170531)
lists=(0 4 5 6 7 8 9 10 11 12 13)
for d in ${dates[@]}; do
  for l in ${lists[@]} ; do
    fn=data/zhaihehe/$l/day/$d.csv
    if [ -f $fn ] ; then
      if [ `ls -l $fn | awk '{ print $5 }'` -gt 500 ] ; then continue; fi
    fi
    while [ `ps -ef | grep "python3 main.py --zhaihehe" | grep -v grep | wc -l` -gt 12 ] ; do sleep 1 ; done
    echo python3 main.py --web zhaihehe --list $l --type day --date $d
    python3 main.py --web zhaihehe --list $l --type day --date $d &
  done
done

while [ `ps -ef | grep "python3 main.py --web zhaihehe" | grep -v grep | wc -l` -ge 1 ] ; do sleep 1 ; done
echo "rm empty file"
for f in `ls data/zhaihehe/*/day/*.csv` ; do
  if [ `ls -l $f | awk '{ print $5 }'` -le 500 ] ; then echo `ls -l $f` ; fi
  if [ `ls -l $f | awk '{ print $5 }'` -le 500 ] ; then rm -f $f ; fi
done
