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


config="config/momo-rank.json"
python3 main.py --config $config --web momo --type rank --rankType star_hour
python3 main.py --config $config --web momo --type rank --rankType star_potential
python3 main.py --config $config --web momo --type rank --rankType star_day
python3 main.py --config $config --web momo --type rank --rankType star_week
python3 main.py --config $config --web momo --type rank --rankType user_day
python3 main.py --config $config --web momo --type rank --rankType user_week
