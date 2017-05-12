#!/bin/bash

cd /home/yao/files/git/spider
infile="infiles/momo-ids.txt"
python3 main.py --web momo --type web2 --infile $infile &
