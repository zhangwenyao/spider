#!/usr/bin/env python
# -*- coding: utf-8 -*-

from general import config as systemconfig
from liveme.rank import rank
from liveme.graph import graph

config = systemconfig.config


def crawl():

    # rank
    rankType = config['type']['rank']['rankType']
    dateType = config['type']['rank']['dateType']
    for r in rankType:
        for d in dateType:
            rank(type='rank', rankType=r, dateType=d)

    # graph
    graph(rankType='all', dateType='all')
