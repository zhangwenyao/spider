#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import requests
from general import config as systemconfig

config = systemconfig.config


def heat(li, date, type='heat', outfolder=None):
    params = config['type'][type]
    url = '{}/{}?package={}'.format(config['url'], params['api'], li)
    url += '&end_date=' + date
    if not outfolder:
        outfolder = li
    fld = os.path.join('data', config['args'].web, outfolder)
    if not os.path.exists(fld):
        os.makedirs(fld)

    print('crawl url: ', url)
    html = requests.get(url)
    data = json.loads(html.text)
    if 'data' not in data or len(data['data']) != 2:
        print(type, 'data error.')
        return
    da = data['data']

    filename = os.path.join(fld, '{}-{}-end.txt'.format(date, type))
    with open(filename, 'w') as f:
        d = da['end']
        h = list(d[0].keys())
        h.sort()
        f.write('\t'.join([str(k) for k in h]))
        for i in d:
            f.write('\n' + '\t'.join([str(i[k]).strip() for k in h]))
    print('save file', filename)

    filename = os.path.join(fld, '{}-{}-mid.txt'.format(date, type))
    with open(filename, 'w') as f:
        d = da['mid']
        h = list(d[0].keys())
        h.sort()
        f.write('\t'.join([str(k) for k in h]))
        for i in d:
            f.write('\n' + '\t'.join([str(i[k]).strip() for k in h]))
    print('save file', filename)


def detailinfo(li, date, type='detailinfo', outfolder=None):
    params = config['type'][type]
    url = '{}/{}?package={}'.format(config['url'], params['api'], li)
    url += '&end_date=' + date
    if not outfolder:
        outfolder = li
    fld = os.path.join('data', config['args'].web, outfolder)
    if not os.path.exists(fld):
        os.makedirs(fld)

    print('crawl url: ', url)
    html = requests.get(url)
    data = json.loads(html.text)
    if 'data' not in data or len(data['data']) != 1:
        print(type, 'data error.')
        return
    da = data['data']

    filename = os.path.join(fld, '{}-{}.txt'.format(date, type))
    with open(filename, 'w') as f:
        d = da[0]
        h = list(d.keys())
        h.sort()
        for i in ('app_info', 'icon'):
            h.remove(i)
        f.write('\n'.join([k + '\t' + str(d[k]) for k in h]))
    print('save file', filename)


def crowddis(li, date, type='crowddis', outfolder=None):
    params = config['type'][type]
    url = '{}/{}?package={}'.format(config['url'], params['api'], li)
    if not outfolder:
        outfolder = li
    fld = os.path.join('data', config['args'].web, outfolder)
    if not os.path.exists(fld):
        os.makedirs(fld)

    print('crawl url: ', url)
    html = requests.get(url)
    data = json.loads(html.text)
    if 'data' not in data or len(data['data']) != 1:
        print(type, 'data error.')
        return
    da = data['data'][0]

    h = list(da.keys())
    h.sort()
    for i in h:
        filename = os.path.join(fld, '{}-{}-{}.txt'.format(date, type, i))
        d = da[i]
        d = d.replace(',', '\n')
        d = d.replace(':', '\t')
        with open(filename, 'w') as f:
            f.write(d)
        print('save file', filename)


def index(li, date, date2, type='index', outfile=None, outfolder=None):
    params = config['type'][type]
    url = '{}/{}?package={}'.format(config['url'], params['api'], li)
    url += '&start_date=' + date
    url += '&end_date=' + date2
    if not outfolder:
        outfolder = li
    fld = os.path.join('data', config['args'].web, outfolder)
    if not os.path.exists(fld):
        os.makedirs(fld)

    print('crawl url: ', url)
    html = requests.get(url)
    data = json.loads(html.text)
    if 'data' not in data:
        print(type, 'data error.')
        return
    da = data['data']

    date = da['date'][:8]
    date2 = da['date'][-8:]
    d = da['value']['num']
    d = d.replace(',', '\n')
    if not outfile:
        outfile = '{}-{}-{}.txt'.format(date, date2, type)
    filename = os.path.join(fld, outfile)
    with open(filename, 'w') as f:
        f.write(d)
    print('save file', filename)
