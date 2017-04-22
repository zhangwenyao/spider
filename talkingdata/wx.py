#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import json
import datetime
import requests
from general import config as systemconfig

config = systemconfig.config


def crawl(type, typeId, date, outfile, outfolder):
    d = {
        'year': int(date[0:4]),
        'month': int(date[4:6]),
        'day': int(date[6:8])
    }
    d1 = datetime.date(d['year'], d['month'], d['day'])
    if d1.weekday():
        d1 -= datetime.timedelta(days=d1.weekday())
        date = d1.strftime("%Y%m%d")
        d = {
            'year': int(date[0:4]),
            'month': int(date[4:6]),
            'day': int(date[6:8])
        }

    api = '{}/{}'.format(config['web'], config[type]['api'])
    if int(typeId) > 0:
        api += '?typeId=' + typeId
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
        outfile = '{}.{}.txt'.format(date, typeId)
    filename = os.path.join(fld, outfile)
    print('save as:', filename)
    with open(filename, 'w') as f:
        data = re.sub('},{', '}\n{', data[1:-1]).split('\n')
        head = list(json.loads(data[0]).keys())
        head.sort()
        f.write('\t'.join(head) + '\n')
        for i in data:
            if i:
                d = json.loads(i)
                f.write('\t'.join(
                    [str(d[k]) if k in d else '' for k in head]) + '\n')

    return
