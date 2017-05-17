#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime
import calendar
import re
import requests
import os
from bs4 import BeautifulSoup
import csv
from general import config as systemconfig

config = systemconfig.config


def crawl(list, date, type='d', date2=None, outfolder=None):
    d = {
        'year': int(date[0:4]),
        'month': int(date[4:6]),
        'day': int(date[6:8])
    }
    d['time'] = calendar.timegm(time.struct_time(
        (d['year'], d['month'], d['day'], -8, 0, 0, 0, 0, 0)))

    if type in ('d', 'day'):
        url = '{}/{}/{}-{}-{}'.format(config['api']['day'], list,
                                      date[0:4], date[4:6], date[6:8])
        if not outfolder:
            outfolder = 'day'
        fld = os.path.join('data', config['args'].web, list, outfolder)
        filename = os.path.join(fld, str(date) + '.csv')

    elif type in ('w', 'week'):
        d1 = datetime.date(d['year'], d['month'], d['day'])
        if d1.weekday():
            d1 -= datetime.timedelta(days=d1.weekday())
            date = d1.strftime("%Y%m%d")
            d = {
                'year': int(date[0:4]),
                'month': int(date[4:6]),
                'day': int(date[6:8])
            }
            d['time'] = calendar.timegm(time.struct_time(
                (d['year'], d['month'], d['day'], -8, 0, 0, 0, 0, 0)))
        date2 = (d1 + datetime.timedelta(days=6)).strftime("%Y%m%d")
        d_2_time = d['time'] + 3600 * 24 * 6
        url = '{}/{}/{}-{}'.format(config['api']['week'], list,
                                   d['time'], d_2_time)
        if not outfolder:
            outfolder = 'week'
        fld = os.path.join('data', config['args'].web, list, outfolder)
        filename = os.path.join(fld, '{}-{}.csv'.format(date, date2))

    elif type in ('m', 'month'):
        d['day'] = 1
        d1 = datetime.date(d['year'], d['month'], d['day'])
        date = d1.strftime("%Y%m%d")
        d['time'] = calendar.timegm(time.struct_time(
            (d['year'], d['month'], d['day'], -8, 0, 0, 0, 0, 0)))
        d_2_day = calendar.monthrange(d['year'], d['month'])[1]
        d_2_time = d['time'] + 3600 * 24 * d_2_day - 1
        d2 = datetime.date(d['year'], d['month'], d_2_day)
        date2 = d2.strftime("%Y%m%d")
        url = '{}/{}/{}-{}'.format(config['api']['month'], list,
                                   d['time'], d_2_time)
        if not outfolder:
            outfolder = 'month'
        fld = os.path.join('data', config['args'].web, list, outfolder)
        filename = os.path.join(fld, '{}-{}.csv'.format(date, date2))

    elif type in ('o', 'other'):
        if not date2:
            print('error: need date2.')
            return None
        d_2 = {
            'year': int(date2[0:4]),
            'month': int(date2[4:6]),
            'day': int(date2[6:8])
        }
        d_2['time'] = calendar.timegm(time.struct_time(
            (d_2['year'], d_2['month'], d_2['day'], 24 - 8, 0, 0, 0, 0, 0))) - 1
        url = '{}/{}/{}-{}'.format(config['api']['month'], list,
                                   d['time'], d_2['time'])
        if not outfolder:
            outfolder = 'other'
        fld = os.path.join('data', config['args'].web, list, outfolder)
        filename = os.path.join(fld, '{}-{}.csv'.format(date, date2))

    else:
        print('type error: {}'.format(type))
        return None

    if not os.path.exists(fld):
        os.makedirs(fld)

    print('crawl url: ', url)
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'lxml')

    td_th = re.compile('t[dh]')
    table = soup.find("table", {"id": "table_header"})
    cells = table.find("tr").findAll(td_th)
    header = [cell.find(text=True).strip() for cell in cells]
    datas = []
    table = soup.find("table", {"id": "table_list"})
    for row in table.findAll("tr"):
        cells = row.findAll(td_th)
        t = cells[1].findAll("h4")[1].find(text=True)
        w_row = [t.strip() if t else '']
        for cell in cells[2:]:
            t = cell.find(text=True)
            w_row.append(t.strip() if t else '')
        datas.append(w_row)
    if len(datas) > 0:
        print('save as: ', filename)
        with open(filename, 'w') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(header)
            for i in datas:
                csv_writer.writerow(i)
    else:
        print('data is empty:', url, filename)

    return None
