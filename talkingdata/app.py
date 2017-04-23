#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import json
import datetime
import requests
from general import config as systemconfig

config = systemconfig.config


def trend(type, typeId, appId, date, date2=None, dateType=None, outfile=None, outfolder=None):
    # "minDay":"2016-01-01"
    # "minWeek":"2017-04-10"
    # "minWeek":"2015-01-05"
    # "maxWeek":"2017-04-10"
    # "minMonth":"2015-03-01"
    # "maxMonth":"2017-03-01"
    # "minQ":"2016-01-01"
    # "maxQ":"2016-10-01"

    if not dateType:
        dateType = 'd'
    if dateType not in config[type]['dateType']:
        print("DateType has to be set properly with --dateType.")
        print('Valid DateType:\n\t', config[type]['dateType'])
        return
    d = {
        'year': int(date[0:4]),
        'month': int(date[4:6]),
        'day': int(date[6:8])
    }
    d1 = datetime.date(d['year'], d['month'], d['day'])
    if not date2:
        date2 = date
    d2 = {
        'year': int(date2[0:4]),
        'month': int(date2[4:6]),
        'day': int(date2[6:8])
    }
    d_2 = datetime.date(d2['year'], d2['month'], d2['day'])
    if dateType == 'w':
        d1 = datetime.date(d['year'], d['month'], d['day'])
        if d1.weekday():
            d1 -= datetime.timedelta(days=d1.weekday())
        d_2 = datetime.date(d2['year'], d2['month'], d2['day'])
        if d_2.weekday():
            d_2 -= datetime.timedelta(days=d_2.weekday())
    elif dateType == 'm':
        d1 = datetime.date(d['year'], d['month'], 1)
        d_2 = datetime.date(d2['year'], d2['month'], 1)
    elif dateType == 'q':
        d1 = datetime.date(d['year'], (d['month'] - 1) // 3 * 3 + 1, 1)
        d_2 = datetime.date(d2['year'], (d2['month'] - 1) // 3 * 3 + 1, 1)

    api = '{}/{}/trend/{}/{}.json'.format(config['web'], config[type]['api'],
                                          appId, config[type]['typeId'][typeId])
    api += '?dateType=' + dateType
    api += '&startTime=' + d1.strftime("%Y-%m-%d")
    api += '&endTime=' + d_2.strftime("%Y-%m-%d")
    print(type, 'crawl:', api)
    data = requests.get(api).text
    if not data or len(data) < 4:
        print('data is empty')
        return
    data = re.sub('},{', '}\n{', data[1:-1]).split('\n')
    if len(data) != 2:
        print('data error.')
        return
    data = [json.loads(i) for i in data]

    if not outfolder:
        outfolder = config[type]['typeId'][typeId]
    fld = os.path.join('data', config['args'].web, type, outfolder)
    if not os.path.exists(fld):
        os.makedirs(fld)
    if not outfile:
        outfile = '{}.{}-{}.{}.txt'.format(
            appId, d1.strftime("%Y%m%d"), d_2.strftime("%Y%m%d"), dateType)
    filename = os.path.join(fld, outfile)
    print('save as:', filename)
    with open(filename, 'w') as f:
        head = [i['name'] for i in data]
        head.sort()
        f.write('\t'.join(head) + '\n')
        data = [i['value'] for i in data]
        data = list(zip(*data))
        for i in data:
            f.write('\t'.join([str(k) for k in i]) + '\n')

    return


def profile(type, typeId, appId, date, outfile=None, outfolder=None):
    # minMonth: 20160101
    d1 = datetime.date(int(date[0:4]), int(date[4:6]), 1)
    api = '{}/{}/profile/{}.json'.format(
        config['web'], config[type]['api'], appId)
    api += '?startTime=' + d1.strftime("%Y-%m-%d")
    print(type, 'crawl:', api)
    data = requests.get(api).text
    if not data or len(data) < 4:
        print('data is empty')
        return
    data = re.sub('\]},{', ']}\n{', data[1:-1]).split('\n')
    if not data:
        print('data error.')
        return
    # for i in data:
        # print('aaa', i)
        # print(json.loads(i))
        # return
    data = [json.loads(i) for i in data]

    if not outfolder:
        outfolder = config[type]['typeId'][typeId]
    fld = os.path.join('data', config['args'].web, type, outfolder)
    if not os.path.exists(fld):
        os.makedirs(fld)
    if not outfile:
        outfile = '{}.{}'.format(appId, d1.strftime("%Y%m%d"))
    filename = os.path.join(fld, outfile)
    for key in data:
        fn = '{}.{}.txt'.format(filename, key['profileName'])
        val = key['profileValue']
        if not val:
            print(fn, 'is empty.')
            continue
        print('save', fn)
        with open(fn, 'w') as f:
            head = list(val[0].keys())
            head.sort()
            f.write('\t'.join(head) + '\n')
            for i in val:
                f.write('\t'.join([str(i[h]) for h in head]) + '\n')
    return
