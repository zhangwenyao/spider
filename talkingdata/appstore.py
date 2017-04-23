#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import requests
from general import config as systemconfig

config = systemconfig.config


def crawl(type, typeId, date, rankType=None, outfile=None, outfolder=None):
    if not rankType:
        rankType = 'rank'
    if rankType not in config[type]['rankType']:
        print("RankType has to be set properly with --rankType.")
        print('Valid RankType:\n\t', config[type]['rankType'])
        return

    api = '{}/{}/{}.json?cat={}&date={}-{}-{}&tab=1'.format(
        config['web'], config[type]['api'], rankType, typeId,
        date[0:4], date[4:6], date[6:8])
    print(type, 'crawl:', api)
    data = json.loads(requests.get(api).text)['rows']
    if not data:
        print('data is empty')
        return

    if not outfolder:
        outfolder = type
    fld = os.path.join('data', config['args'].web, outfolder)
    if not os.path.exists(fld):
        os.makedirs(fld)
    if not outfile:
        outfile = '{}.{}.{}.txt'.format(date, typeId, rankType)
    filename = os.path.join(fld, outfile)
    print('save as:', filename)
    with open(filename, 'w') as f:
        head = list(data[0].keys())
        head.remove('appinfo')
        head.sort()
        head2 = list(data[0]['appinfo'].keys())
        head2.sort()
        f.write('\t'.join(head + head2) + '\n')
        for i in data:
            f.write('\t'.join(
                [str(i[k]) if k in i else '' for k in head] +
                [str(i['appinfo'][k]) if k in i['appinfo'] else '' for k in head2]) + '\n')

    return
