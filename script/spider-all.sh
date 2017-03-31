#!/bin/bash

if [ $(($#%2)) -eq 1 ] ; then
    echo "usage : $0 [-d 20170101] [-2 20170203]"
    exit 1
fi

lists=(4 5 6 7 8 9 10 11 12 13)
for l in ${lists[@]} ; do
    echo python3 live.py -l $l $@
    python3 live.py -l $l $@
done

