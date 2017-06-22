#!/bin/bash
echo `date '+%Y%m%d-%H%M%S'` $0


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


cmd="python3 main.py --web momo --config config/momo.json --type web-counts-day"
echo "$cmd"
echo "$cmd" | sh


dir="export/momo/star-day"
outfile="star-day-join"
ids=(347074466 334370152 338561490 337153000 79046028  55284359  384870563 86977431  333848639 456841345 336400734 81660978  332001566 29399418  466494697 5081208 415134950 345436454)

#echo "join star-day files > ../$outfile"
cd $dir
d1="20170513"
#d2=`date '+%Y%m%d' -d '1 day ago'`
d2=`date '+%Y%m%d'`
outfile="../$outfile-$d1-$d2.txt"
if [ -f $outfile ] ; then exit 1 ; fi
n=0
header="#date"
for id in ${ids[@]} ;  do
  #echo $id
  header="$header $id"
  if [ $n -eq 0 ] ; then
    cmd="cat $id-$d1-$d2.txt"
  else
    cmd="$cmd | join - $id-$d1-$d2.txt"
  fi
  let "n+=1"
done
echo -e $header > $outfile
cmd="$cmd >> $outfile"
echo "$cmd"
echo "$cmd" | sh
