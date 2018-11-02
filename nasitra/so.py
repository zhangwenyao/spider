#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from general import config as systemconfig

config = systemconfig.config


def baiduMOTA(args):
    type = list(config['type'].keys())
    type.append('all')
    if not args.type:
        args.type = 'all'
    if args.type not in type:
        logging.info("Type has to be set properly with -t/--type.")
        logging.info('Valid List:\n\t' + type)
        return

    if not args.list:
        args.list = 'FPD9'   # momo
    if len(args.list) != 4:
        logging.info("List has to be set as 4 letters with -l/--list.")
        return

    if args.type == 'dailyCrawl':
        from baidu.dailyCrawl import crawl
        return crawl()

    if args.type == 'heat':
        from baidu.motaApp import heat
        heat(li=args.list, date=args.date,
             type=args.type, outfolder=args.outfolder)
        return

    if args.type == 'detailinfo':
        from baidu.motaApp import detailinfo
        detailinfo(li=args.list, date=args.date,
                   type=args.type, outfolder=args.outfolder)
        return

    if args.type == 'crowddis':
        from baidu.motaApp import crowddis
        crowddis(li=args.list, date=args.date,
                 type=args.type, outfolder=args.outfolder)
        return

    if args.type == 'index':
        from baidu.motaApp import index
        index(li=args.list, date=args.date, date2=args.date2,
              type=args.type, outfile=args.outfile, outfolder=args.outfolder)
        return
