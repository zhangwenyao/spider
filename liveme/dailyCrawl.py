#!/usr/bin/env python
# -*- coding: utf-8 -*-

from general import config as systemconfig
from datetime import datetime,timedelta
from liveme.graph import graph

config = systemconfig.config


def crawl():
    exact_time = datetime.utcnow() + timedelta(hours=8)
    if exact_time.hour < 23:
        return


    # graph
    graph(rankType='all', dateType='all')
