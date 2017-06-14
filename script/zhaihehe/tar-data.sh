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


dir=data/zhaihehe
for m in $(seq 1 4) ; do
  (cd ${dir}/0/day && rm 20170${m}??.csv && pwd)
  for i in $(seq 4 13) ; do
    (cd ${dir}/${i}/day && rm -f 20170${m}??.csv && pwd)
  done
done

