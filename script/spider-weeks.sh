#!/bin/bash

file="script/weeks_lists.txt"
if [ ! -f "${file}" ]; then
    exit 1
fi

lists=(0 4 5 6 7 8 9 10 11 12 13)
cat ${file} | while read line ; do
    for l in ${lists[@]} ; do
        echo python3 live.py -t week -l $l ${line}
        python3 live.py -t week -l $l ${line}
    done
done
