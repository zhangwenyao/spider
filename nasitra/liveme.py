#!/usr/bin/env python

# -*- coding: utf-8 -*-

import logging
from general import config as systemconfig

config = systemconfig.config


def liveme(args):

    type = list(config['type'].keys())
    if not args.type:
        args.type = 'rank'
    if args.type not in type:
        logging.info("Type has to be set properly with -t/--type.")
        logging.info('Valid List:\n\t' + type)
        return

    if args.type == 'dailyCrawl':
        from liveme.dailyCrawl import crawl
        return crawl()

    if args.type == 'rank':
        from liveme.rank import rank
        return rank(rankType=args.rankType, dateType=args.dateType,
                    type=args.type, outfolder=args.outfolder)

    if args.type == 'graph':
        from liveme.graph import graph
        return graph(rankType=args.rankType, dateType=args.dateType)
