#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import re
import requests
from bs4 import BeautifulSoup
import csv
from general import config as systemconfig


def crawl(list, outfolder, date, d2=None):
    date1 = int(time.mktime(time.strptime(date, '%Y%m%d')))
    if d2:
        date2 = int(time.mktime(time.strptime(d2, '%Y%m%d'))) - 1 + 3600 * 24
        filename = 'data/{}/{}/{}-{}.csv'.format(list, outfolder, date, d2)
    else:
        date2 = date1 - 1 + 3600 * 24
        filename = 'data/{}/{}/{}.csv'.format(list, outfolder, date)
    url = '{}/{}/{}-{}'.format(systemconfig.api, list, date1, date2)
    print(url)

    html = requests.get(url)
    with open('test/4.html', 'w') as f:
        f.write(html.text)
    soup = BeautifulSoup(html.text, 'lxml')

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
