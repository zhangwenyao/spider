#!/bin/bash

dir="data/momo/star-day"
outfile="star-day-join.txt"
ids=(347074466 334370152 338561490 337153000 79046028  55284359  384870563 86977431  333848639 456841345 336400734 81660978  332001566 29399418  466494697 5081208 415134950 345436454)

header="date"
n=0
cd $dir
for id in ${ids[@]} ;  do
  echo $id
  header="$header\t$id"
  if [ $n -eq 0 ] ; then
    cmd="cat $id.txt"
  else
    cmd="$cmd | join -t '	' - $id.txt"
  fi
  let "n+=1"
done
echo -e $header > ../$outfile
echo $cmd
echo "$cmd >> ../$outfile" | sh
