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


appIds=(189)
typeIds=(1 2 3)
for appId in ${appIds[@]} ; do
  for typeId in ${typeIds[@]} ; do
    while [ `ps -ef | grep "python3 main.py" | grep -v grep | wc -l` -gt 12 ] ; do sleep 1 ; done
    cmd="python3 main.py --web talkingdata --type app --listname $appId --list $typeId --dateType d &"
    echo "$cmd"
    echo "$cmd" | sh
  done
done
