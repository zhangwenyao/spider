#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import csv
import logging
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from general import config as systemconfig

config = systemconfig.config
filesize = 100


def crawl(date=None, list='0', city='0', sex='0', fans='0', outfolder=None,
          range1='1', range2='0'):
    fld = date if date else (
        datetime.now() - timedelta(hours=24 - 8)).strftime("%Y%m%d")
    url = '{}_{}_{}_{}'.format(list, city, sex, fans)
    # if list or city or sex or fans:
    fld += '.' + url
    if not outfolder:
        outfolder = 'anchor'
    fld = os.path.join(config['folders']['datadir'], config['args'].web,
                       list, outfolder, fld)
    if not os.path.exists(fld):
        os.makedirs(fld)

    url = '{}/{}'.format(config['api']['anchor'], url)
    if not range1:
        range1 = 1
    else:
        range1 = int(range1)
    if not range2:
        range2 = 0
    else:
        range2 = int(range2)
    if range2 <= 0:
        logging.info('crawl url: ' + url)
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'lxml')
        num = str(soup.find('li', {'id': 'Page_End'}))
        num = re.sub("[\s\S]*p=", '', num)
        num = re.sub('"[\s\S]*', '', num)
        num = int(num) if num != 'None' else 0
        logging.info('Number of pages: {}'.format(num))
        range2 = num
        fn = os.path.join(fld, '1.csv')
        if range1 <= 1 and (not os.path.exists(fn) or os.path.getsize(fn) < filesize):
            head = anchor_head(soup)
            if not head:
                logging.info('error: page 1 data head is empty')
            else:
                rows = [head]
                flag = True
                table = soup.find(
                    "div", {"class": "table-body company-list-body"})
                for row in table.findAll("div", {"class": "table-row ng-scope"}):
                    data = anchor_row(row)
                    if not data:
                        flag = False
                    else:
                        rows.append(data)
                if not flag:
                    logging.info('error: page 1 data row is empty')
                else:
                    logging.info('save as: ' + fn)
                    with open(fn, 'w') as f:
                        csv_writer = csv.writer(f)
                        for r in rows:
                            csv_writer.writerow(r)
            range1 = 2
    for i in range(range1, range2 + 1):
        url2 = '{}/&p={}'.format(url, i)
        fn = os.path.join(fld, str(i) + '.csv')
        if not os.path.exists(fn) or os.path.getsize(fn) < filesize:
            try:
                anchor_page(url2, fn)
            except:
                logging.info('error: crawl ' + url2)
    return


def anchor_head(t):
    t = t.find("div", {"id": "table_title"})
    t = re.sub('<!--', '', str(t))
    t = re.sub('-->', '', t)
    t = re.sub('\s*<[^>]*>\s*', '\t', t)
    t = re.sub('\t+', '\t', t)
    t = t.strip().split('\t')
    if not t:
        logging.debug('error: table head is empty')
        return
    return [x.strip() for x in t]


def anchor_row(t):
    name = t.find('div', {'class': 'name'})
    name = name.get_text() if name else ''
    d = t.findAll('div', {'class': 'table-col founder'})
    id = d[0].get_text()
    t = re.sub('[\s\S]*<div class="table-col founder">', '', str(t))
    t = re.sub('<div class="table-col"></div>', 'null', str(t))
    t = re.sub('<!--', '', str(t))
    t = re.sub('-->', '', t)
    t = re.sub('\s*<[^>]*>\s*', '\t', t)
    t = re.sub('\t+', '\t', t)
    data = [name, id] + t.split('\t')
    if not data:
        logging.debug('error: table is empty')
        return
    return [x.strip() for x in data]


def anchor_page(url, fn):
    logging.info('crawl url: ' + url)
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'lxml')
    head = anchor_head(soup)
    if not head:
        logging.debug('error: head is empty')
        return
    rows = [head]
    flag = True
    table = soup.find("div", {"class": "table-body company-list-body"})
    for row in table.findAll("div", {"class": "table-row ng-scope"}):
        data = anchor_row(row)
        if not data:
            flag = False
            logging.debug('error: data is empty')
        else:
            rows.append(data)
    if not flag:
        return
    logging.info('save as: ' + fn)
    with open(fn, 'w') as f:
        csv_writer = csv.writer(f)
        for r in rows:
            csv_writer.writerow(r)
    return


def momoIds(infolder=None, outfolder=None):
    if not infolder:
        infolder = os.path.join(config['folders']['datadir'], config['args'].web,
                                '8', 'anchor')
        flds = [x for x in os.listdir(infolder)
                if os.path.isdir(os.path.join(infolder, x))]
        if not flds:
            return
        flds.sort()
        infolder = os.path.join(infolder, flds[-1])
    if not outfolder:
        outfolder = os.path.join(
            config['folders']['exportdir'], config['args'].web)
    if not os.path.exists(outfolder):
        os.mkdirs(outfolder)
    elif not os.path.isdir(outfolder):
        logging.debug('path error: ' + outfolder)
        return
    date = (datetime.now() - timedelta(hours=24 - 8)).strftime("%Y%m%d")
    fn = os.path.join(outfolder, 'momoIds_{}.txt'.format(date))

    if not os.path.exists(infolder) or not os.path.isdir(infolder):
        logging.info('path error: ' + infolder)
        return
    files = [x for x in os.listdir(infolder)
             if x.endswith('.csv')
             and os.path.isfile(os.path.join(infolder, x))
             and os.path.getsize(os.path.join(infolder, x)) >= filesize]
    datas = {}
    for x in files:
        with open(os.path.join(infolder, x), 'r') as f:
            csv_reader = csv.DictReader(f)
            for r in csv_reader:
                if '主播ID' not in r:
                    # logging.info('data format error: ' + x)
                    # return
                    print('error', x)
                    continue
                datas[r['主播ID']] = x[:-4]
    keys = list(datas.keys())
    keys = [int(x) for x in keys]
    keys.sort()
    if not keys:
        return
    with open(fn, 'w') as f:
        for k in keys:
            f.write('{}\t{}\n'.format(k, datas[str(k)]))
    logging.info('save file: ' + fn)
