#!/bin/bash

cd /home/yao/files/git/spider
infile="infiles/momo-ids.txt"
while true ; do
  python3 main.py --web momo --type web2 --infile $infile >> logs/momo-ids-star.log
done
