#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import os
import re
import requests
from bs4 import BeautifulSoup
from general import config as systemconfig

config = systemconfig.config


def crawl(date=None, list='0', city='0', sex='0', fans='0', outfolder=None,
          range1='0', range2='0'):
    filename = date if date else (
        datetime.datetime.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    url = '{}_{}_{}_{}'.format(list, city, sex, fans)
    if list or city or sex or fans:
        filename += '.' + url
    if not outfolder:
        outfolder = 'anchor'
    fld = os.path.join('data', config['args'].web, list, outfolder, filename)
    if not os.path.exists(fld):
        os.makedirs(fld)

    url = '{}/{}'.format(config['api']['anchor'], url)
    range1 = int(range1)
    range2 = int(range2)
    if range1 <= 1 or range2 <= 0:
        print('crawl url:', url)
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'lxml')
        num = str(soup.find('li', {'id': 'Page_End'}))
        num = re.sub("[\s\S]*p=", '', num)
        num = re.sub('"[\s\S]*', '', num)
        num = int(num) if num != 'None' else 0
        print('Num of pages:', num)
        if range2 <= 0 or range2 > num:
            range2 = num
        if range1 <= 1:
            fn = os.path.join(fld, '1.txt')
            print('save as:', fn)
            with open(fn, 'w') as f:
                head = soup.find("div", {"id": "table_title"})
                f.write(anchor_row(head))
                table = soup.find(
                    "div", {"class": "table-body company-list-body"})
                for row in table.findAll("div", {"class": "table-row ng-scope"}):
                    f.write(anchor_row(row))
            range1 = 2
    for i in range(range1, range2):
        url2 = '{}/&p={}'.format(url, i)
        fn = os.path.join(fld, str(i) + '.txt')
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
