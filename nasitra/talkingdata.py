#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from general import config as systemconfig

config = systemconfig.config


def talkingdata(args):

    type = config['type']
    if not args.type:
        args.type = type[0]
    if args.type not in type:
        print("Type has to be set properly with -t/--type.")
        print('Valid Type:\n\t', type)
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
    if li and args.list not in li:
        print("List has to be set properly with -l/--list.")
        print('Valid List:\n\t', li)
        return

    if args.type == 'app':
        if args.list in ('1', '2', '3'):
            from talkingdata.app import trend
            return trend(type=args.type, typeId=args.list, appId=args.listname,
                         date=args.date, date2=args.date2, dateType=args.dateType,
                         outfile=args.outfile, outfolder=args.outfolder)
        if args.list == '4':
            from talkingdata.app import profile
            return profile(type=args.type, typeId=args.list, appId=args.listname,
                           date=args.date,
                           outfile=args.outfile, outfolder=args.outfolder)
        print(args.type, 'error.')
        return

    if not args.date:
        args.date = (datetime.datetime.today() -
                     datetime.timedelta(days=1)).strftime("%Y%m%d")
    if len(args.date) != 8:
        print("Date has to be set properly in '20170101' form.")
        return

    if args.type == 'apprank':
        from talkingdata.apprank import crawl
        return crawl(type=args.type, typeId=args.list, rankType=args.rankType,
                     date=args.date, dateType=args.dateType,
                     outfile=args.outfile, outfolder=args.outfolder)

    if args.type == 'wx':
        from talkingdata.wx import crawl
        return crawl(type=args.type, categoryId=args.list, date=args.date,
                     outfile=args.outfile, outfolder=args.outfolder)

    if args.type == 'appstore':
        from talkingdata.appstore import crawl
        return crawl(type=args.type, typeId=args.list, rankType=args.rankType, date=args.date,
                     outfile=args.outfile, outfolder=args.outfolder)

    if args.type == 'terminals':
        from talkingdata.terminals import crawl
        return crawl(type=args.type, terminalType=args.list, platform=args.rankType,
                     date=args.date, dateType=args.dateType,
                     outfile=args.outfile, outfolder=args.outfolder)

    if args.type == 'market':
        from talkingdata.market import crawl
        return crawl(type=args.type, date=args.date,
                     outfile=args.outfile, outfolder=args.outfolder)

    print('Type error:', args.type)
    return
