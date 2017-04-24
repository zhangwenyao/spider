#!/bin/bash

dates=(20170101 20170102 20170103 20170104 20170105 20170106 20170107 20170108 20170109 \
  20170110 20170111 20170112 20170113 20170114 20170115 20170116 20170117 20170118 20170119 \
  20170120 20170121 20170122 20170123 20170124 20170125 20170126 20170127 20170128 20170129 \
  20170130 20170131)
lists=(0 4 5 6 7 8 9 10 11 12 13)
for d in ${dates[@]}; do
  for l in ${lists[@]} ; do
    while [ `ps -ef | grep "python3 live.py" | grep -v grep | wc -l` -gt 12 ] ; do sleep 1 ; done
    echo python3 live.py --list $l --type day --date $d
    python3 live.py --list $l --type day --date $d &
  done
done
