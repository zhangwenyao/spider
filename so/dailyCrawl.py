#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from datetime import datetime, timedelta
from baidu.motaApp import detailinfo, index, heat, crowddis


def crawl():

    li = 'FPD9'  # momo

    # detailinfo
    for i in range(1, 5):
        date = (datetime.today() - timedelta(days=31 * i)
                ).strftime('%Y%m') + '01'
        detailinfo(li=li, date=date)

    # index
    date2 = index(li=li)
    if date2:
        logging.info('new data, date: ' + date2)
        crowddis(li=li, date=date2)
        heat(li=li, date=date2)
