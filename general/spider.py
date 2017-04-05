#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import calendar
import re
import requests
import os
from bs4 import BeautifulSoup
import csv
from general import config as systemconfig


def crawl(list, type, date, date2=None, outfolder=None):
    d = {
        'year': int(date[0:4]),
        'month': int(date[4:6]),
        'day': int(date[6:8])
    }
    d['time'] = calendar.timegm(time.struct_time(
        (d['year'], d['month'], d['day'], -8, 0, 0, 0, 0, 0)))

    if type in ('d', 'day'):
        url = '{}/{}/{:0>4d}-{:0>2d}-{:0>2d}'.format(systemconfig.api['day'], list,
                                                     d['year'], d['month'], d['day'])
        if not outfolder:
            outfolder = 'day'
        fld = 'data/{}/{}'.format(list, outfolder)
        filename = '{}/{}.csv'.format(fld, date)

    elif type in ('w', 'week'):
        if not date2:
            print('error: need date2.')
            return None
        d2 = {
            'year': int(date2[0:4]),
            'month': int(date2[4:6]),
            'day': int(date2[6:8])
        }
        d2['time'] = calendar.timegm(time.struct_time(
            (d2['year'], d2['month'], d2['day'], -8, 0, 0, 0, 0, 0)))
        url = '{}/{}/{}-{}'.format(systemconfig.api['week'], list,
                                   d['time'], d2['time'])
        if not outfolder:
            outfolder = 'week'
        fld = 'data/{}/{}'.format(list, outfolder)
        filename = '{}/{}-{}.csv'.format(fld, date, date2)

    elif type in ('m', 'month'):
        d['day'] = 1
        d['time'] = calendar.timegm(time.struct_time(
            (d['year'], d['month'], d['day'], -8, 0, 0, 0, 0, 0)))
        d2 = {
            'year': d['year'],
            'month': d['month'],
            'day': calendar.monthrange(int(d['year']), int(d['month']))[1]
        }
        d2['time'] = d['time'] + 3600 * 24 * int(d2['day']) - 1
        url = '{}/{}/{}-{}'.format(systemconfig.api['month'], list,
                                   d['time'], d2['time'])
        if not outfolder:
            outfolder = 'month'
        fld = 'data/{}/{}'.format(list, outfolder)
        filename = '{}/{:0>4d}{:0>2d}{:0>2d}-{:0>4d}{:0>2d}{:0>2d}.csv'.format(
            fld, d['year'], d['month'], d['day'],
            d2['year'], d2['month'], d2['day'])

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
        url = '{}/{}/{}-{}'.format(systemconfig.api['month'], list,
                                   d['time'], d2['time'])
        if not outfolder:
            outfolder = 'other'
        fld = 'data/{}/{}'.format(list, outfolder)
        filename = '{}/{}-{}.csv'.format(fld, date, date2)

    else:
        print('type error: {}'.format(type))
        return None

    if not os.path.exists(fld):
        os.mkdir(fld)

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
