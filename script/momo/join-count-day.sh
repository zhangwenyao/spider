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


cmd="python3 script/momo/count-day.py"
echo "$cmd"
echo "$cmd" | sh


dir="data/momo/star-day"
outfile="star-day-join.txt"
ids=(347074466 334370152 338561490 337153000 79046028  55284359  384870563 86977431  333848639 456841345 336400734 81660978  332001566 29399418  466494697 5081208 415134950 345436454)

#echo "join star-day files > $outfile"
header="date"
n=0
cd $dir
for id in ${ids[@]} ;  do
  #echo $id
  header="$header\t$id"
  if [ $n -eq 0 ] ; then
    cmd="cat $id.txt"
  else
    cmd="$cmd | join -t '	' - $id.txt"
  fi
  let "n+=1"
done
echo -e $header > ../$outfile
cmd="$cmd >> ../$outfile"
echo "$cmd"
echo "$cmd" | sh
