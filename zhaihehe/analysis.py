#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import csv
from general import config as systemconfig

config = systemconfig.config


def analysis(list, listname, infolder, outfile, outfolder=None):
    if not listname:
        print('listname should be a string.')
        return
    fldin = os.path.join('data', config['args'].web, list, infolder)
    if not os.path.isdir(fldin):
        print('error: infolder should be a folder.')
        return
    l = os.listdir(fldin)
    files = [x for x in l if os.path.isfile(os.path.join(fldin, x))]
    if not files:
        print(fldin, l, files)
        return
    files.sort()

    if not outfolder:
        outfolder = 'analysis'
    fld = os.path.join('data', config['args'].web, list, outfolder)
    if not os.path.exists(fld):
        os.makedirs(fld)

    data = []
    n = 0
    for file in files:
        with open(os.path.join(fldin, file), 'r') as f:
            f_csv = csv.DictReader(f)
            if infolder in ('day', 'week'):
                h = ['{}-{}-{}'.format(file[0:4], file[4:6], file[6:8])]
            elif infolder == 'month':
                h = ['{}-{}'.format(file[0:4], file[4:6])]
            elif infolder.endswith('.csv'):
                h = [infolder[0:-4]]
            else:
                h = [file]
            d = [row[listname] for row in f_csv]
            if len(d) < 1:
                print('error: file {} is empty.'.format(file))
                continue
            if n == 0:
                n = len(d)
            if n != len(d):
                print('error: length of file {} is not {}.'.format(file, n))
                continue
            h.append(sum([int(x) for x in d]))
            h.extend(d)
            data.append(h)
            print(file)

    fn = os.path.join(fld, outfile)
    print('save as:', fn)
    with open(fn, 'w') as f:
        # for row in zip(*data):
        for row in data:
            k = '\t'.join([str(c) for c in row])
            f.write(k + "\n")

    return None
