#!/bin/bash

appIds=(189)
for appId in ${appIds[@]} ; do
  cmd="python3 main.py --web talkingdata --type app --listname $appId --list 4"
  echo $cmd
  echo $cmd | sh
done
