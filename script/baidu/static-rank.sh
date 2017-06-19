#!/bin/bash
echo `date` $0


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


cmd="python3 main.py --web baidu --type graph --rankType detailRank"
echo "$cmd"
echo "$cmd" | sh

