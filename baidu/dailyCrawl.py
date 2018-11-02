#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from datetime import datetime, timedelta
from baidu.motaApp import detailinfo, index, heat, crowddis
from baidu.graph import graph
from general import config as systemconfig

config = systemconfig.config


def crawl(li=None):
    exact_time = datetime.utcnow() + timedelta(hours=8)
    if exact_time.hour < 23:
        return

    if not li:
        li = config['list']

    # li = 'FPD9'  # momo

    # detailinfo
    for i in range(1, 5):
        date = (datetime.today() - timedelta(days=31 * i)
                ).strftime('%Y%m') + '01'
        detailinfo(li=li, date=date)
    graph(rankType='detailRank', li=li)

    # index
    date2 = index(li=li)
    if date2:
        logging.info('new data, date: ' + date2)
        crowddis(li=li, date=date2)
        heat(li=li, date=date2)
    graph(rankType='index', li=li)
