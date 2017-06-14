#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import datetime
import requests
import logging
from general import config as systemconfig

config = systemconfig.config


def heat(li, date, type='heat', outfolder=None):
    if not outfolder:
        outfolder = li
    fld = os.path.join('data', config['args'].web, outfolder)
    filename1 = os.path.join(fld, '{}-{}-end.txt'.format(date, type))
    filename2 = os.path.join(fld, '{}-{}-mid.txt'.format(date, type))
    if os.path.exists(filename1) and os.path.exists(filename2):
        return
    if not os.path.exists(fld):
        os.makedirs(fld)

    params = config['type'][type]
    url = '{}/{}?package={}'.format(config['url'], params['api'], li)
    url += '&end_date=' + date
    logging('crawl url: ' + url)
    html = requests.get(url)
    data = json.loads(html.text)
    if 'data' not in data or len(data['data']) != 2:
        logging.info(type + ' data error.')
        return
    da = data['data']

    with open(filename1, 'w') as f:
        d = da['end']
        h = list(d[0].keys())
        h.sort()
        f.write('\t'.join([str(k) for k in h]))
        for i in d:
            f.write('\n' + '\t'.join([str(i[k]).strip() for k in h]))
    logging.info('save file: ' + filename1)

    with open(filename2, 'w') as f:
        d = da['mid']
        h = list(d[0].keys())
        h.sort()
        f.write('\t'.join([str(k) for k in h]))
        for i in d:
            f.write('\n' + '\t'.join([str(i[k]).strip() for k in h]))
    logging.info('save file: ' + filename2)


def detailinfo(li, date=None, type='detailinfo', outfolder=None):
    # minDate='20141201'
    if not date:
        date = (datetime.datetime.today() -
                datetime.timedelta(days=1)).strftime("%Y%m") + '01'
    if not outfolder:
        outfolder = li
    fld = os.path.join('data', config['args'].web, outfolder)
    filename = os.path.join(fld, '{}-{}.txt'.format(date, type))
    if os.path.exists(filename):
        return
    if not os.path.exists(fld):
        os.makedirs(fld)

    params = config['type'][type]
    url = '{}/{}?package={}'.format(config['url'], params['api'], li)
    url += '&end_date=' + date
    logging.info('crawl url: ' + url)
    html = requests.get(url)
    data = json.loads(html.text)
    if 'data' not in data or len(data['data']) != 1:
        logging.info(type + ' data error.')
        return
    da = data['data']

    with open(filename, 'w') as f:
        d = da[0]
        h = list(d.keys())
        h.sort()
        for i in ('app_info', 'icon'):
            h.remove(i)
        f.write('\n'.join([k + '\t' + str(d[k]) for k in h]))
    logging.info('save file: ' + filename)


def crowddis(li, date, type='crowddis', outfolder=None):
    params = config['type'][type]
    url = '{}/{}?package={}'.format(config['url'], params['api'], li)
    if not outfolder:
        outfolder = li
    fld = os.path.join('data', config['args'].web, outfolder)
    if not os.path.exists(fld):
        os.makedirs(fld)

    logging.info('crawl url: ' + url)
    html = requests.get(url)
    data = json.loads(html.text)
    if 'data' not in data or len(data['data']) != 1:
        logging.info(type + ' data error.')
        return
    da = data['data'][0]

    h = list(da.keys())
    h.sort()
    for i in h:
        filename = os.path.join(fld, '{}-{}-{}.txt'.format(date, type, i))
        if os.path.exists(filename):
            logging.info('file exists: ' + filename)
            continue
        d = da[i]
        d = d.replace(',', '\n')
        d = d.replace(':', '\t')
        with open(filename, 'w') as f:
            f.write(d)
        logging.info('save file: ' + filename)


def index(li, date=None, date2=None, type='index', outfile=None, outfolder=None):
    if not date:
        date = '20141201'
    if len(date) != 8:
        logging.info(
            "Date has to be set as in '20170101' form with -d/--date.")
        return
    if not date2:
        date2 = (datetime.datetime.today() -
                 datetime.timedelta(days=1)).strftime("%Y%m%d")
    if len(date2) != 8:
        logging.info(
            "Date2 has to be set as in '20170101' form with -2/--date2.")
        return

    if not outfolder:
        outfolder = li
    fld = os.path.join('data', config['args'].web, outfolder)
    if not os.path.exists(fld):
        os.makedirs(fld)
    if not outfile:
        filename = '{}-{}-{}.txt'.format(date, date2, type)
    else:
        filename = outfile
    filename = os.path.join(fld, filename)
    if os.path.exists(filename):
        # logging.info('file exists: ' + filename)
        return

    params = config['type'][type]
    url = '{}/{}?package={}'.format(config['url'], params['api'], li)
    url += '&start_date=' + date
    url += '&end_date=' + date2
    logging.info('crawl url: ' + url)
    html = requests.get(url)
    data = json.loads(html.text)
    if 'data' not in data:
        logging.info(type + ' data error.')
        return
    da = data['data']

    date = da['date'][:8]
    date2 = da['date'][-8:]
    d = da['value']['num']
    d = d.replace(',', '\n')
    if not outfile:
        filename = '{}-{}-{}.txt'.format(date, date2, type)
    else:
        filename = outfile
    filename = os.path.join(fld, filename)
    if os.path.exists(filename):
        logging.info('file exists: ' + filename)
        return
    with open(filename, 'w') as f:
        f.write(d)
    logging.info('save file: ' + filename)
    return date2
