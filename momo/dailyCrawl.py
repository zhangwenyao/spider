#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import subprocess
from general import config as systemconfig
from momo.count import day
from momo.graph import graph

config = systemconfig.config


def crawl():

    # web count
    day()

    # join count day
    try:
        sh = os.path.join('script', 'momo', 'join-count-day.sh')
        out_bytes = subprocess.check_output(sh, stderr=subprocess.STDOUT,
                                            shell=True)
    except subprocess.CalledProcessError as e:
        out_bytes = e.output
        logging.info('join-count-day error')
        logging.debug(out_bytes)

    graph(rankType='starDay')
    graph(rankType='rankStarHour')
    graph(rankType='rankStarHour2')
