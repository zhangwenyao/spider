#!/bin/bash

lists=(FPD9)
for l in ${lists[@]} ; do
  echo python3 main.py --web baidu --type heat --list $l
  python3 main.py --web baidu --type heat --list $l
done
