#!/bin/bash

dir=data/zhaihehe
for m in $(seq 1 4) ; do
  (cd ${dir}/0/day && rm 20170${m}??.csv && pwd)
  for i in $(seq 4 13) ; do
    (cd ${dir}/${i}/day && rm -f 20170${m}??.csv && pwd)
  done
done

