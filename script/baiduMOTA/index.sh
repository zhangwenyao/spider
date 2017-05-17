#!/bin/bash

lists=(FPD9)
for l in ${lists[@]} ; do
  echo python3 main.py --web baiduMOTA --type index --list $l --date 20170101 --date2 20171231
  python3 main.py --web baiduMOTA --type index --list $l --date 20170101 --date2 20171231
done
