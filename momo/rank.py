#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from datetime import datetime, timedelta
import requests
import json
import logging
from general import config as systemconfig

config = systemconfig.config


def rank(rankType, outfolder=None):
    if not outfolder:
        outfolder = rankType
    fld = os.path.join('data', config['args'].web, 'rank', outfolder)
    if not os.path.exists(fld):
        os.makedirs(fld)

    t = datetime.utcnow() + timedelta(hours=8)
    dt = t.minute % 15
    t = t - timedelta(minutes=dt)
    filename = os.path.join(fld, t.strftime('%Y%m%d-%H%M') + '.txt')
    # if rankType == 'star_potential':
        # t = datetime.utcnow() + timedelta(hours=8)
        # dt = t.minute % 15
        # t = t - timedelta(minutes=dt)
        # filename = os.path.join(fld, t.strftime('%Y%m%d-%H%M') + '.txt')
    # elif rankType == 'star_hour':
        # t = datetime.utcnow() + timedelta(hours=8)
        # dt = t.minute % 15
        # t = t - timedelta(minutes=dt)
        # filename = os.path.join(fld, t.strftime('%Y%m%d-%H%M') + '.txt')
    # elif rankType == 'star_day':
        # t = datetime.utcnow() + timedelta(hours=8)
        # dt = t.hour % 12
        # t = t - timedelta(hours=dt)
        # filename = os.path.join(fld, t.strftime('%Y%m%d-%H') + '.txt')
    # elif rankType == 'star_week':
        # t = datetime.utcnow() + timedelta(hours=8)
        # filename = os.path.join(fld, t.strftime('%Y%m%d') + '.txt')
    # elif rankType == 'user_day':
        # t = datetime.utcnow() + timedelta(hours=8)
        # dt = t.hour % 12
        # t = t - timedelta(hours=dt)
        # filename = os.path.join(fld, t.strftime('%Y%m%d-%H') + '.txt')
    # elif rankType == 'user_week':
        # t = datetime.utcnow() + timedelta(hours=8)
        # filename = os.path.join(fld, t.strftime('%Y%m%d') + '.txt')
    # else:
        # logging.info('rankType error: ' + rankType)
        # return

    if os.path.exists(filename) and os.path.getsize(filename) > 100:
        # logging.info('file already exists: {}'.format(filename))
        return

    try:
        url = '{}{}'.format(config['rank']['api'], rankType)
        logging.info('crawl url: {}'.format(url))
        html = requests.get(url)
        data = json.loads(html.text)
        data = data['data']['lists']
        if not len(data):
            raise
        logging.info('save as file: {}'.format(filename))
        heads = list(data[0].keys())
        heads.sort()
        with open(filename, 'w') as f:
            f.write('\t'.join(heads) + '\n')
            for i in data:
                f.write('\t'.join([str(i[c]) for c in heads]) + '\n')
    except:
        logging.info('data error')
