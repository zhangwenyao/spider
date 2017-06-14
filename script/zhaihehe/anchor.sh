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


file="data/zhaihehe/anchor-lists.txt"
if [ ! -f "${file}" ]; then
  echo error
  exit 1
fi

#lists=(0 4 5 6 7 8 9 10 11 12 13)
cat ${file} | while read line
do
  while [ `ps -ef | grep "python3 main.py --web zhaihehe" | grep -v grep | wc -l` -ge 8 ] ; do sleep 1 ; done
  echo python3 main.py --web zhaihehe --type anchor --date 20170423 --list 8 --range1 ${line} --range2 ${line}
  python3 main.py --web zhaihehe --type anchor --date 20170423 --list 8 --range1 ${line} --range2 ${line} &
  sleep 1
done
