#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from zhaihehe.lists import crawl as listsCrawl


def crawl():
    exact_time = datetime.utcnow() + timedelta(hours=8)
    if exact_time.hour < 23:
        return

    lists = ('0', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13')

    # day
    for i in range(1, 8):
        date = (datetime.today() - timedelta(days=i)).strftime("%Y%m%d")
        for l in lists:
            listsCrawl(list=l, date=date, type='day')

    # week
    for i in range(1, 4):
        date = (datetime.today() - timedelta(days=7 * i)).strftime("%Y%m%d")
        for l in lists:
            listsCrawl(list=l, date=date, type='week')

    # month
    for i in range(1, 4):
        date = (datetime.today() - timedelta(days=31 * i)).strftime("%Y%m%d")
        for l in lists:
            listsCrawl(list=l, date=date, type='month')
