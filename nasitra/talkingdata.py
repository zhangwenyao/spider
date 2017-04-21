#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from general import config as systemconfig

config = systemconfig.config


def talkingdata(args):

    type = config['type']
    if not args.type:
        args.type = 'app'
    if args.type not in type:
        print("Type has to be set properly with -t/--type.")
        print('Valid Type:\n\t', type)
        return

    if not args.date:
        args.date = (datetime.datetime.today() -
                     datetime.timedelta(days=1)).strftime("%Y%m%d")
    if len(args.date) != 8:
        print("Date has to be set properly in '20170101' form.")
        return

    li = []
    if config[args.type]['typeId']:
        li.extend(list(config[args.type]['typeId'].keys()))
    if config[args.type]['typeId2']:
        for (k, v) in config[args.type]['typeId2'].items():
            if k not in li:
                print('Config file error: {}: typeId2 {} not in typeId.'.format(
                    args.type, k))
                return
            if v:
                li.extend([i for i in v])
    if not args.list and li:
        args.list = str(min([int(i) for i in li]))
    if args.list not in li:
        print("List has to be set properly with -l/--list.")
        print('Valid List:\n\t', li)
        return

    if args.type == 'app':
        from talkingdata.app import crawl
        return crawl(type=args.type, typeId=args.list, rankType=args.rankType,
                     date=args.date, dateType=args.dateType,
                     outfile=args.outfile, outfolder=args.outfolder)

    print('Type error:', args.type)
    return
