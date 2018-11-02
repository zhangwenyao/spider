#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests
from bs4 import BeautifulSoup
import logging
from general import config as systemconfig

config = systemconfig.config


def news():
    dir = os.path.join(config['folders']['datadir'],
                       config['args'].web)
    dir2 = os.path.join(dir,'news')
    if not os.path.exists(dir):
        os.makedirs(dir)

    filename = os.path.join(config['folders']['datadir'],
                            config['args'].web, 'news.txt')
    news = []
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            datas = f.readlines()

        datas = [x.strip().split('\t') for x in datas[1:]]
        news = [{'date': x[0], 'url':x[1], 'title':x[2]} for x in datas]

    page = 1
    n2 = []
    flag = True
    while flag:
        n = get_page(page=page)
        if not n:
            break
        for x in n:
            if newsInPage(x, news):
                flag = False
                break
            else:
                n2.insert(0, x)

        page += 1

    if not n2:
        return

    news.extend(n2)
    with open(filename, 'w') as f:
        f.write('#date\turl\ttitle\n')
        for n in news:
            f.write('{}\t{}\t{}\n'.format(n['date'], n['url'], n['title']))
            try:
                ourfile = os.path.join(config['folders']['datadir'], config['args'].web,
                                       'news', url[32:])
            except:
                pass

    logging.info('save file: ' + filename)


def newsInPage(news, page):
    flag = False
    for x in page:
        if x['url'] == news['url']:
            flag = True
            break

    return flag


def get_page(page):
    url = '{}/{}'.format(config['news']['api'], page)
    logging.info('crawl url: ' + url)
    news = []
    try:
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'lxml')
        for s in soup.findAll('section'):
            data = {
                'url':    '{}{}'.format(config['html']['homepage'], s.a['href']),
                'title':    s.a.string.strip(),
                'date': s.find('p', {'class': 'date'}).string,
                # 'note': s.find('div', {'class': 'note_clear_fix'}).string,
                'line2':    s.find('p', {'class': 'line2'}).string
            }
            if data:
                news.append(data)
    except:
        logging.debug('data error: ' + url)
        if news:
            return news
        else:
            return None


def html(url, outfile):
    try:
        h = requests.get(url)
        soup = BeautifulSoup(h.text, 'lxml')
        s = soup.findAll('section')
        with open(outfile, 'w') as f:
            f.write(s)

        logging.info('save file: {}'.format(outfile))
    except:
        logging.info('get news error: {}'.format(url))

