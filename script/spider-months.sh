#!/bin/bash

dates=(20170101 20170201 20170301)
lists=(0 4 5 6 7 8 9 10 11 12 13)
for d in ${dates[@]} ; do
    for l in ${lists[@]} ; do
        echo python3 live.py -l $l -t month -d ${d}
        python3 live.py -l $l -t month -d ${d}
    done
done
