#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import os
import re
import requests
from bs4 import BeautifulSoup
from general import config as sc


def anchor(outfile=None, list=0, city=0, sex=0, fans=0, outfolder=None,
           range1=0, range2=0):
    if not outfolder:
        outfolder = 'anchor'
    fld = 'data/{}'.format(outfolder)
    if not os.path.exists(fld):
        os.mkdir(fld)
    filename = outfile if outfile else (
        datetime.datetime.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    url = '{}_{}_{}_{}'.format(list, city, sex, fans)
    if list or city or sex or fans:
        filename += '.' + url
    fn = '{}/{}.1.txt'.format(fld, filename)

    url = '{}/{}'.format(sc.config['api']['anchor'], url)
    print('crawl url:', url)
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'lxml')
    num = str(soup.find('li', {'id': 'Page_End'}))
    num = re.sub("[\s\S]*p=", '', num)
    num = re.sub('"[\s\S]*', '', num)
    num = int(num)
    print(num, 'pages')

    if range1 == 0:
        print('save as:', fn)
        with open(fn, 'w') as f:
            head = soup.find("div", {"id": "table_title"})
            f.write(anchor_row(head))
            table = soup.find("div", {"class": "table-body company-list-body"})
            for row in table.findAll("div", {"class": "table-row ng-scope"}):
                f.write(anchor_row(row))
        range1 = 2

    if range2 == 0:
        range2 = num
    for i in range(range1, range2):
        url2 = '{}/&p={}'.format(url, i)
        fn = '{}/{}.{}.txt'.format(fld, filename, i)
        anchor_page(url2, fn)

    return


def anchor_row(t):
    name = t.find('div', {'class': 'name'})
    if name is None:
        name = ''
        t = str(t)
    else:
        name = name.get_text().strip() + '\t'
        t = re.sub('[\s\S]*<div class="table-col founder">', '', str(t))
    t = re.sub('<!--', '', str(t))
    t = re.sub('-->', '', t)
    t = re.sub('\s*<[^>]*>\s*', '\t', t)
    t = re.sub('\t+', '\t', t)
    return name + t.strip() + '\n'


def anchor_page(url, fn):
    print('craul url:', url)
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'lxml')
    print('save as:', fn)
    with open(fn, 'w') as f:
        head = soup.find("div", {"id": "table_title"})
        f.write(anchor_row(head))
        table = soup.find("div", {"class": "table-body company-list-body"})
        for row in table.findAll("div", {"class": "table-row ng-scope"}):
            f.write(anchor_row(row))
    return
