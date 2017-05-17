#!/bin/bash

lists=(FPD9)
for l in ${lists[@]} ; do
  echo python3 main.py --web baiduMOTA --type heat --list $l
  python3 main.py --web baiduMOTA --type heat --list $l
done
