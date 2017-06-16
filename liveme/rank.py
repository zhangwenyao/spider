#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
from datetime import datetime, timedelta
import requests
import logging
from general import config as systemconfig

config = systemconfig.config


def rank(type=None, rankType=None, dateType=None, outfolder=None):
    if not type:
        type = 'rank'
    params = config['type'][type]
    if not rankType:
        rankType = params['rankType'][0]
    if not dateType:
        dateType = params['dateType'][0]
    if not outfolder:
        outfolder = type
    fld = os.path.join('data', config['args'].web, outfolder,
                       rankType + '-' + dateType)
    if not os.path.exists(fld):
        os.makedirs(fld)


    t = datetime.utcnow() + timedelta(hours=8)
    dt = t.minute % 15
    t = t - timedelta(minutes=dt)
    filename = os.path.join(fld, t.strftime('%Y%m%d-%H%M') + '.txt')
    # if dateType == 'week':
        # t = datetime.utcnow() + timedelta(hours=8)
        # filename = os.path.join(fld, t.strftime('%Y%m%d') + '.txt')
    # else:   # 'day', 'total'
        # t = datetime.utcnow() + timedelta(hours=8)
        # dt = t.hour % 12
        # t = t - timedelta(hours=dt)
        # filename = os.path.join(fld, t.strftime('%Y%m%d-%H') + '.txt')
    if os.path.exists(filename):
        return

    url = '{}/{}/{}{}rank'.format(config['url'], params['api'], rankType,
                                  dateType)
    logging.info('crawl url: ' + url)
    html = requests.get(url)
    data = json.loads(html.text)
    if 'data' not in data or len(data['data']) < 1:
        logging.info(type + ' data error.')
        return
    da = data['data']

    h = list(da[0].keys())
    h.sort()
    if 'usign' in h:
        h.remove('usign')
    with open(filename, 'w') as f:
        f.write('\t'.join([str(k) for k in h]))
        for i in da:
            f.write('\n' + '\t'.join([str(i[k]).strip() for k in h]))
    logging.info('save file: ' + filename)
