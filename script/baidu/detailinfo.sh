#!/bin/bash

lists=(FPD9)
for l in ${lists[@]} ; do
  echo python3 main.py --web baiduMOTA --type detailinfo --list $l
  python3 main.py --web baiduMOTA --type detailinfo --list $l
done
