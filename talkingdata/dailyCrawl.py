#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from talkingdata.app import trend, profile, all


def crawl_1():

    appId = '189'

    # trend
    typeIds = ('1', '2', '3')

    # day
    for i in range(1, 8):
        date2 = (datetime.today() - timedelta(days=i)).strftime("%Y%m%d")
        for typeId in typeIds:
            trend(type='app', typeId=typeId, appId=appId,
                  date2=date2, dateType='d')

    # week
    date2 = (datetime.today() - timedelta(days=7)).strftime("%Y%m%d")
    for typeId in typeIds:
        trend(type='app', typeId=typeId, appId=appId,
              date2=date2, dateType='w')

    # month
    date2 = (datetime.today() - timedelta(days=31)).strftime("%Y%m%d")
    for typeId in typeIds:
        trend(type='app', typeId=typeId, appId=appId,
              date2=date2, dateType='m')

    # quarter
    date2 = (datetime.today() - timedelta(days=93)).strftime("%Y%m%d")
    for typeId in typeIds:
        trend(type='app', typeId=typeId, appId=appId,
              date2=date2, dateType='q')

    # profile monthly
    profile(type='app', typeId='4', appId=appId)


def crawl():

    appId = '189'

    # trend
    typeId = '0'
    # day
    all(type='app', typeId=typeId, appId=appId, dateType='d')
    # week
    all(type='app', typeId=typeId, appId=appId, dateType='w')
    # month
    all(type='app', typeId=typeId, appId=appId, dateType='m')
    # quarter
    all(type='app', typeId=typeId, appId=appId, dateType='q')

    # profile monthly
    typeId = '4'
    profile(type='app', typeId=typeId, appId=appId)
