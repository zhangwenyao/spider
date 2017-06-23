#!/usr/bin/env python
# -*- coding: utf-8 -*-

from general import config as systemconfig
from liveme.graph import graph

config = systemconfig.config


def crawl():

    # graph
    graph(rankType='all', dateType='all')
