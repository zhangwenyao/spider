#!/bin/bash

date1=20170301
date2=20170331
lists=(4 5 6 7 8 9 10 11 12 13)
for l in ${lists[@]} ; do
    echo python3 live.py -o month -l $l -d ${date1} -2 ${date2}
    python3 live.py -o month -l $l -d ${date1} -2 ${date2}
done
