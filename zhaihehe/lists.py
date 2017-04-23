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
        d2_time = d['time'] + 3600 * 24 * 6
        url = '{}/{}/{}-{}'.format(config['api']['week'], list,
                                   d['time'], d2_time)
        if not outfolder:
            outfolder = 'week'
        fld = os.path.join('data', config['args'].web, list, outfolder)
        filename = os.path.join(fld, '{}-{}.csv'.format(date, date2))

    elif type in ('m', 'month'):
        date[6:8] = '01'
        d['day'] = 1
        d['time'] = calendar.timegm(time.struct_time(
            (d['year'], d['month'], d['day'], -8, 0, 0, 0, 0, 0)))
        d2_day = calendar.monthrange(d['year'], d['month'])[1]
        d2_time = d['time'] + 3600 * 24 * d2_day - 1
        date2 = date
        date2[6:8] = '%2d' % d2_day
        url = '{}/{}/{}-{}'.format(config['api']['month'], list,
                                   d['time'], d2_time)
        if not outfolder:
            outfolder = 'month'
        fld = os.path.join('data', config['args'].web, list, outfolder)
        filename = os.path.join(fld, '{}-{}.csv'.format(date, date2))

    elif type in ('o', 'other'):
        if not date2:
            print('error: need date2.')
            return None
        d2 = {
            'year': int(date2[0:4]),
            'month': int(date2[4:6]),
            'day': int(date2[6:8])
        }
        d2['time'] = calendar.timegm(time.struct_time(
            (d2['year'], d2['month'], d2['day'], 24 - 8, 0, 0, 0, 0, 0))) - 1
        url = '{}/{}/{}-{}'.format(config['api']['month'], list,
                                   d['time'], d2['time'])
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

    print('save as: ', filename)
    f = open(filename, 'w')
    csv_writer = csv.writer(f)
    td_th = re.compile('t[dh]')

    table = soup.find("table", {"id": "table_header"})
    for row in table.findAll("tr"):
        cells = row.findAll(td_th)
        csv_writer.writerow([cell.find(text=True).strip() for cell in cells])
    table = soup.find("table", {"id": "table_list"})

    for row in table.findAll("tr"):
        cells = row.findAll(td_th)
        t = cells[1].findAll("h4")[1].find(text=True)
        w_row = [t.strip() if t else '']
        for cell in cells[2:]:
            t = cell.find(text=True)
            w_row.append(t.strip() if t else '')
        csv_writer.writerow(w_row)
    f.close()

    return None
