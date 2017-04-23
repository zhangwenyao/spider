#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import json
import datetime
import requests
from general import config as systemconfig

config = systemconfig.config


def crawl(type, typeId, date, rankType=None, dateType=None, outfile=None, outfolder=None):
    # "minWeek":"2015-01-05"
    # "minMonth":"2015-03-01"
    # "minQ":"2016-01-01"
    # 移动应用排行榜：选定周期内，按应用的覆盖率进行排行。
    # 成长应用潜力排行：选定周期内，根据覆盖率变化幅度，选取0.05%≤覆盖率＜1%的应用进行排名。
    # 新兴应用潜力排行：选定周期内，根据覆盖率变化幅度，选取0.005%≤覆盖率＜0.05%的应用进行排名。
    # 覆盖率：安装此应用的活跃设备量/监测活跃设备总量。
    # 活跃率：开启此应用的活跃设备量/监测活跃设备总量。

    if not rankType:
        rankType = 'a'
    if rankType not in config[type]['rankType']:
        print("RankType has to be set properly with --rankType.")
        print('Valid RankType:\n\t', config[type]['rankType'])
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
    elif dateType == 'q':
        d['month'] = (d['month'] - 1) // 3 * 3 + 1
        d['day'] = 1
    date = '{:0>4d}{:0>2d}{:0>2d}'.format(d['year'], d['month'], d['day'])

    api = '{}/{}?date={}-{}-{}'.format(
        config['web'], config[type]['api'], date[0:4], date[4:6], date[6:8])
    if int(typeId) > 0:
        api += '&typeId=' + typeId
    api += '&rankType=' + rankType
    api += '&dateType=' + dateType
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
            date, typeId, rankType, dateType)
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


def trend_ranking():
    pass


def trend_coverageRate():
    pass


def trend_activeRate():
    pass


def profile():
    # minMonth: 20160101
    pass
