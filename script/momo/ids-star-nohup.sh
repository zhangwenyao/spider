#!/bin/bash

cd /home/yao/files/git/spider
infile="infiles/momo-ids.txt"
while true ; do
  date
  echo "python3 main.py --web momo --type web2 --list 10 --infile $infile >> logs/momo-ids-star.log"
  python3 main.py --web momo --type web2 --list 10 --infile $infile >> logs/momo-ids-star.log
done
