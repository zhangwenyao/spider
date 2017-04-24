#!/bin/bash

dates=(20170301 20170302 20170303 20170304 20170305 20170306 20170307 20170308 20170309 \
  20170310 20170311 20170312 20170313 20170314 20170315 20170316 20170317 20170318 20170319 \
  20170320 20170321 20170322 20170323 20170324 20170325 20170326 20170327 20170328 20170329 \
  20170330 20170331)
lists=(0 4 5 6 7 8 9 10 11 12 13)
for d in ${dates[@]}; do
  for l in ${lists[@]} ; do
    while [ `ps -ef | grep "python3 live.py" | grep -v grep | wc -l` -gt 12 ] ; do sleep 1 ; done
    echo python3 live.py --list $l --type day --date $d
    python3 live.py --list $l --type day --date $d &
  done
done
