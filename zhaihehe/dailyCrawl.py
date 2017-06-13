#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from zhaihehe.lists import crawl as listsCrawl


def crawl():
    lists = ('0', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13')

    # day
    for i in range(1, 8):
        date = (datetime.today() - timedelta(days=i)).strftime("%Y%m%d")
        for l in lists:
            listsCrawl(list=l, date=date, type='day')

    # week
    date = (datetime.today() - timedelta(days=7)).strftime("%Y%m%d")
    for l in lists:
        listsCrawl(list=l, date=date, type='week')

    # month
    date = (datetime.today() - timedelta(days=31)).strftime("%Y%m%d")
    for l in lists:
        listsCrawl(list=l, date=date, type='month')
