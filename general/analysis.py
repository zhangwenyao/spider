#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import csv


def analysis(listname, list, infolder, outfile, outfolder=None):
    if not listname:
        print('listname should be a string.')
        return
    infolder = 'data/{}/{}/'.format(list, infolder)
    if not os.path.isdir(infolder):
        print('error: infolder should be a folder.')
        return
    l = os.listdir(infolder)
    files = [x for x in l if os.path.isfile(infolder + x)]
    if not files:
        return

    if not outfolder:
        outfolder = 'analysis'
    fld = 'data/{}/{}/'.format(list, outfolder)
    if not os.path.exists(fld):
        os.mkdir(fld)

    data = []
    n = 0
    for file in files:
        with open(infolder + file) as f:
            f_csv = csv.DictReader(f)
            d = [file]
            d.extend([row[listname] for row in f_csv])
            if len(d) <= 1:
                print('error: file {} is empty.'.format(file))
                continue
            if n == 0:
                n = len(d)
            if n != len(d):
                print('error: length of file {} is not {}.'.format(file, n))
                continue
            data.append(d)

    print('save as:', fld + outfile)
    with open(fld + outfile, 'w') as f:
        # for row in data:
        for row in zip(*data):
            k = '\t'.join([str(c) for c in row])
            f.write(k + "\n")

    return None
