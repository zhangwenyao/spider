#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import json
import datetime
import requests
from general import config as systemconfig

config = systemconfig.config


def crawl(type, terminalType,  date, platform=None, dateType=None, outfile=None, outfolder=None):
    # 品牌排行说明：品牌：此品牌下活跃设备量/监测活跃设备总量。
    # "minWeek":"0001-01-10",
    # "minMonth":"2014-01-01",
    # "minQ":"2014-01-01"

    if terminalType == '1':
        platform = '3'
    else:
        if not platform:
            platform = '2'
        if platform not in ('1', '2'):
            print("Platform has to be set properly with --rankType.")
            print('Valid Platform:\n\t', ('1', '2'))
            return

    if not dateType:
        dateType = 'w'
    if dateType not in config[type]['dateType']:
        print("DateType has to be set properly with --dateType.")
        print('Valid DateType:\n\t', config[type]['dateType'])
        return
    d = {
        'year': int(date[0:4]),
        'month': int(date[4:6]),
        'day': int(date[6:8])
    }
    if dateType == 'w':
        d1 = datetime.date(d['year'], d['month'], d['day'])
        if d1.weekday():
            d1 -= datetime.timedelta(days=d1.weekday())
            date = d1.strftime("%Y%m%d")
            d = {
                'year': int(date[0:4]),
                'month': int(date[4:6]),
                'day': int(date[6:8])
            }
    elif dateType == 'm':
        d['day'] = 1
    elif dateType in ('q'):
        d['month'] = (d['month'] - 1) // 3 * 3 + 1
        d['day'] = 1
    date = '{:0>4d}{:0>2d}{:0>2d}'.format(d['year'], d['month'], d['day'])

    api = '{}/{}?date={}-{}-{}'.format(
        config['web'], config[type]['api'], date[0:4], date[4:6], date[6:8])
    api += '&dateType=' + dateType
    api += '&platform=' + platform
    api += '&terminalType=' + terminalType
    print(type, 'crawl:', api)
    data = requests.get(api).text
    if not data or len(data) < 4:
        print('data is empty')
        return

    if not outfolder:
        outfolder = type
    fld = os.path.join('data', config['args'].web, outfolder)
    if not os.path.exists(fld):
        os.makedirs(fld)
    if not outfile:
        outfile = '{}.{}.{}.{}.txt'.format(
            date, terminalType, platform, dateType)
    filename = os.path.join(fld, outfile)
    print('save as:', filename)
    with open(filename, 'w') as f:
        data = re.sub('}\s*,\s*{', '}\n{', data[1:-1]).split('\n')
        head = list(json.loads(data[0]).keys())
        head.sort()
        f.write('\t'.join(head) + '\n')
        for i in data:
            if i:
                d = json.loads(i)
                f.write('\t'.join(
                    [str(d[k]) if k in d else '' for k in head]) + '\n')

    return
