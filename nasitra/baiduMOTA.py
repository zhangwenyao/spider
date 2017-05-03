#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from general import config as systemconfig

config = systemconfig.config


def baiduMOTA(args):
    type = list(config['type'].keys())
    type.append('all')
    if not args.type:
        args.type = 'all'
    if args.type not in type:
        print("Type has to be set properly with -t/--type.")
        print('Valid List:\n\t', type)
        return

    if not args.list:
        args.list = 'FPD9'   # momo
    if len(args.list) != 4:
        print("List has to be set as 4 letters with -l/--list.")
        return

    if not args.date:
        args.date = (datetime.datetime.today() -
                     datetime.timedelta(days=1)).strftime("%Y%m%d")
    if len(args.date) != 8:
        print("Date has to be set as 20170101 with -d/--date.")
        return

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
        if not args.date2:
            print("Date2 has to be set properly with -2/--date2.")
            return
        if len(args.date2) != 8:
            print("Date2 has to be set properly in '20170101' form.")
            return
        from baidu.motaApp import index
        index(li=args.list, date=args.date, date2=args.date2,
              type=args.type, outfile=args.outfile, outfolder=args.outfolder)
        return
