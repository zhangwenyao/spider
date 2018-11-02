#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import json
import datetime
import requests
import logging
from general import config as systemconfig

config = systemconfig.config


def trend(type, typeId, appId=None, date=None, date2=None, dateType=None, outfile=None, outfolder=None):
    minDay = '20160101'
    minWeek = '20150105'
    minMonth = '20150301'
    minQ = '20160101'

    if not dateType:
        dateType = 'd'
    if dateType not in config[type]['dateType']:
        logging.info("DateType has to be set properly with --dateType.")
        logging.info('Valid DateType:\n\t' + config[type]['dateType'])
        return

    if not date2:
        date2 = (datetime.datetime.utcnow() + datetime.timedelta(hours=8) -
                 datetime.timedelta(days=1)).strftime("%Y%m%d")
    d_2 = datetime.datetime.strptime(date2, '%Y%m%d')

    if dateType == 'd':
        if not date:
            date = minDay
        d_1 = datetime.datetime.strptime(date, '%Y%m%d')
    if dateType == 'w':
        if not date:
            date = minWeek
        d_1 = datetime.datetime.strptime(date, '%Y%m%d')
        if d_1.weekday():
            d_1 -= datetime.timedelta(days=d_1.weekday())
            date = d_1.strftime('%Y%m%d')
        if d_2.weekday():
            d_2 -= datetime.timedelta(days=d_2.weekday())
            date2 = d_2.strftime('%Y%m%d')
    elif dateType == 'm':
        if not date:
            date = minMonth
        d_1 = datetime.datetime.strptime(date, '%Y%m%d')
        if d_1.day > 1:
            d_1 -= datetime.timedelta(days=d_1.day - 1)
            date = d_1.strftime('%Y%m%d')
        if d_2.day > 1:
            d_2 -= datetime.timedelta(days=d_2.day - 1)
            date2 = d_2.strftime('%Y%m%d')
    elif dateType == 'q':
        if not date:
            date = minQ
        d_1 = datetime.datetime.strptime(date, '%Y%m%d')
        if d_1.month % 3 != 1 or d_1.day > 1:
            d_1 -= datetime.date(int(date[0:4]),
                                 (int(date[4:6]) - 1) // 3 * 3 + 1, 1)
            date = d_1.strftime('%Y%m%d')
        if d_2.month % 3 != 1 or d_2.day > 1:
            d_2 = datetime.date(int(date2[0:4]),
                                (int(date2[4:6]) - 1) // 3 * 3 + 1, 1)
            date2 = d_2.strftime('%Y%m%d')

    if not outfolder:
        outfolder = config[type]['typeId'][typeId]
    fld = os.path.join('data', config['args'].web, type, outfolder)
    if not os.path.exists(fld):
        os.makedirs(fld)
    if not outfile:
        outfile = '{}.{}-{}.{}.txt'.format(
            appId, date, date2, dateType)
    filename = os.path.join(fld, outfile)
    if os.path.exists(filename):
        # logging.info('file already exists: ' + filename)
        return

    api = '{}/{}/trend/{}/{}.json'.format(
        config['web'], config[type]['api'],
        appId, config[type]['typeId'][typeId])
    api += '?dateType=' + dateType
    api += '&startTime=' + d_1.strftime("%Y-%m-%d")
    api += '&endTime=' + d_2.strftime("%Y-%m-%d")
    logging.info(type + ' crawl: ' + api)
    data = requests.get(api).text
    if not data or len(data) < 4:
        logging.info('data is empty')
        return
    data = re.sub('},{', '}\n{', data[1:-1]).split('\n')
    if len(data) != 2:
        logging.info('data error.')
        return
    data = [json.loads(i) for i in data]
    logging.info('save as: ' + filename)
    with open(filename, 'w') as f:
        head = [i['name'] for i in data]
        head.sort()
        f.write('\t'.join(head) + '\n')
        data2 = {}
        for i in data:
            data2[i['name']] = i['value']
        data = list(zip(*[data2[i] for i in head]))
        for i in data:
            f.write('\t'.join([str(k) for k in i]) + '\n')

    return


def profile(type, typeId, appId=None, date=None, outfile=None, outfolder=None):
    # minMonth = '20160101'
    if not date:
        date = (datetime.datetime.utcnow() + datetime.timedelta(hours=8) -
                datetime.timedelta(days=31)).strftime("%Y%m%d")
    d_1 = datetime.date(int(date[0:4]), int(date[4:6]), 1)
    date = d_1.strftime('%Y%m%d')

    if not outfolder:
        outfolder = config[type]['typeId'][typeId]
    fld = os.path.join('data', config['args'].web, type, outfolder)
    if not os.path.exists(fld):
        os.makedirs(fld)
    if not outfile:
        outfile = '{}.{}'.format(appId, date)
    filename = os.path.join(fld, outfile)
    fns = ['age', 'consumption', 'gender', 'preference', 'province']
    flag = True
    for f in fns:
        fn = '{}.{}.txt'.format(filename, f)
        if not os.path.exists(fn) or os.path.getsize(fn) < 10:
            flag = False
            break
    if flag:
        # logging.info('files already exist: ' + filename)
        return

    api = '{}/{}/profile/{}.json'.format(
        config['web'], config[type]['api'], appId)
    api += '?startTime=' + d_1.strftime("%Y-%m-%d")
    logging.info(type + ' crawl: ' + api)
    data = requests.get(api).text
    if not data or len(data) < 4:
        logging.info('data is empty')
        return
    data = re.sub('\]},{', ']}\n{', data[1:-1]).split('\n')
    if not data:
        logging.info('data error.')
        return
    data = [json.loads(i) for i in data]

    for key in data:
        fn = '{}.{}.txt'.format(filename, key['profileName'])
        val = key['profileValue']
        if not val:
            logging.info(fn + ' is empty.')
            continue
        if d_1.strftime('%y-%m-%d') != key['date']:
            logging.info(fn + ' date is error: ' + key['date'])
            continue
        logging.info('save ' + fn)
        with open(fn, 'w') as f:
            head = list(val[0].keys())
            head.sort()
            f.write('\t'.join(head) + '\n')
            for i in val:
                f.write('\t'.join([str(i[h]) for h in head]) + '\n')
    return


def all(type, typeId, appId=None, date=None, date2=None, dateType=None, outfile=None, outfolder=None):
    minDay = '20160101'
    minWeek = '20150105'
    minMonth = '20150301'
    minQ = '20160101'

    if not dateType:
        dateType = 'd'
    if dateType not in config[type]['dateType']:
        logging.info("DateType has to be set properly with --dateType.")
        logging.info('Valid DateType:\n\t' + config[type]['dateType'])
        return

    if not date2:
        date2 = (datetime.datetime.utcnow() + datetime.timedelta(hours=8) -
                 datetime.timedelta(days=1)).strftime("%Y%m%d")
    d_2 = datetime.datetime.strptime(date2, '%Y%m%d')

    if dateType == 'd':
        if not date:
            date = minDay
        d_1 = datetime.datetime.strptime(date, '%Y%m%d')
    if dateType == 'w':
        if not date:
            date = minWeek
        d_1 = datetime.datetime.strptime(date, '%Y%m%d')
        # if d_1.weekday():
        # d_1 -= datetime.timedelta(days=d_1.weekday())
        # date = d_1.strftime('%Y%m%d')
        # if d_2.weekday():
        # d_2 -= datetime.timedelta(days=d_2.weekday())
        # date2 = d_2.strftime('%Y%m%d')
    elif dateType == 'm':
        if not date:
            date = minMonth
        d_1 = datetime.datetime.strptime(date, '%Y%m%d')
        # if d_1.day > 1:
        # d_1 -= datetime.timedelta(days=d_1.day - 1)
        # date = d_1.strftime('%Y%m%d')
        # if d_2.day > 1:
        # d_2 -= datetime.timedelta(days=d_2.day - 1)
        # date2 = d_2.strftime('%Y%m%d')
    elif dateType == 'q':
        if not date:
            date = minQ
        d_1 = datetime.datetime.strptime(date, '%Y%m%d')
        # if d_1.month % 3 != 1 or d_1.day > 1:
        # d_1 -= datetime.date(int(date[0:4]),
        # (int(date[4:6]) - 1) // 3 * 3 + 1, 1)
        # date = d_1.strftime('%Y%m%d')
        # if d_2.month % 3 != 1 or d_2.day > 1:
        # d_2 = datetime.date(int(date2[0:4]),
        # (int(date2[4:6]) - 1) // 3 * 3 + 1, 1)
        # date2 = d_2.strftime('%Y%m%d')

    if not outfolder:
        outfolder = config[type]['typeId'][typeId]
    fld = os.path.join('data', config['args'].web, type, outfolder)
    if not os.path.exists(fld):
        os.makedirs(fld)
    if not outfile:
        filename = '{}.{}-{}.{}.txt'.format(
            appId, date, date2, dateType)
    else:
        filename = outfile
    filename = os.path.join(fld, filename)
    if os.path.exists(filename):
        # logging.info('file already exists: ' + filename)
        return

    api = '{}/{}/trend/{}/allKpi.json'.format(
        config['web'], config[type]['api'], appId)
    api += '?typeIds=1'
    api += '&dateType=' + dateType
    api += '&startDate=' + d_1.strftime("%Y-%m-%d")
    api += '&endDate=' + d_2.strftime("%Y-%m-%d")
    logging.info(type + ' crawl: ' + api)
    try:
        data = requests.get(api).text
        data = json.loads(data[1:-1])
        if 'date' not in data:
            raise
    except:
        logging.info('data error')
        return
    date = data['date'][0].replace('-', '')
    date2 = data['date'][-1].replace('-', '')
    if not outfile:
        filename = '{}.{}-{}.{}.txt'.format(
            appId, date, date2, dateType)
    else:
        filename = outfile
    filename = os.path.join(fld, filename)
    if os.path.exists(filename):
        logging.info('file already exists: ' + filename)
        return
    logging.info('save as: ' + filename)
    heads = list(data.keys())
    heads.sort()
    with open(filename, 'w') as f:
        for k in heads:
            f.write(str(k) + '\t' +
                    '\t'.join([str(i) for i in data[k]]) + '\n')

    return
