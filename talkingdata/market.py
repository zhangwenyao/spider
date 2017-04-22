#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import requests
from general import config as systemconfig

config = systemconfig.config


def crawl(type, date, outfile, outfolder):
    d = {
        'year': int(date[0:4]),
        'month': int(date[4:6]),
        'day': 1
    }
    date = '{:0>4d}{:0>2d}{:0>2d}'.format(d['year'], d['month'], d['day'])

    api = '{}/{}?date={:0>4d}-{:0>2d}-{:0>2d}'.format(
        config['web'], config[type]['api'], d['year'], d['month'], d['day'])
    print(type, 'crawl:', api)
    data = requests.get(api).text
    if not data or len(data) < 4:
        print('data is empty')
        return

    if not outfolder:
        outfolder = type
    fld = os.path.join('data', 'talkingdata', outfolder)
    if not os.path.exists(fld):
        os.mkdir(fld)
    if not outfile:
        outfile = '{}'.format(date)
    data = json.loads(data)
    for (k, v) in data.items():
        filename = os.path.join(fld, outfile + '.' + k + '.txt')
        print('save', k, 'as:', filename)
        with open(filename, 'w') as f:
            head = list(v[0].keys())
            head.sort()
            f.write('\t'.join(head) + '\n')
            for i in v:
                f.write('\t'.join([str(i[j]) for j in head]) + '\n')

    return
