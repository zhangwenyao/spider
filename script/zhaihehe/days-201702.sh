#!/bin/bash

dates=(20170201 20170202 20170203 20170204 20170205 20170206 20170207 20170208 20170209 \
  20170210 20170211 20170212 20170213 20170214 20170215 20170216 20170217 20170218 20170219 \
  20170220 20170221 20170222 20170223 20170224 20170225 20170226 20170227 20170228)
lists=(0 4 5 6 7 8 9 10 11 12 13)
for d in ${dates[@]}; do
  for l in ${lists[@]} ; do
    while [ `ps -ef | grep "python3 live.py" | grep -v grep | wc -l` -gt 12 ] ; do sleep 1 ; done
    echo python3 live.py --list $l --type day --date $d
    python3 live.py --list $l --type day --date $d &
  done
done
