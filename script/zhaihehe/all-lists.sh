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


if [ $(($#%2)) -eq 1 ] ; then
  echo "usage : $0 [-d 20170101] [-2 20170203] [-t {day,week,month,other}]"
  exit 1
fi

lists=(0 4 5 6 7 8 9 10 11 12 13)
for l in ${lists[@]} ; do
  while [ `ps -ef | grep "python3 main.py --web zhaihehe" | grep -v grep | wc -l` -gt 12 ] ; do sleep 1 ; done
  echo python3 main.py --web zhaihehe --list $l $@ &
  python3 main.py --web zhaihehe --list $l $@ &
done

