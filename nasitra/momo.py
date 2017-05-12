#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from general import config as systemconfig

config = systemconfig.config


def momo(args):
    type = config['type']
    if not args.type:
        args.type = 'web'
    if args.type not in type:
        print("Type has to be set properly with -t/--type.")
        print('Valid List:\n\t', type)
        return

    if not list:
        print("List has to be set properly with -l/--list.")
        return

    if not args.date:
        args.date = datetime.datetime.today().strftime("%Y%m%d")
    if len(args.date) != 8:
        print("Date has to be set as 20170101 with -d/--date.")
        return

    if args.type == 'web':
        from momo.web import web
        web(id=args.list, type=args.type, outfolder=args.outfolder)
        return

    if args.type == 'web2':
        if not args.infile:
            print("Infile has to be set properly with -i/--infile.")
            return

        from momo.web import web2
        web2(infile=args.infile, outfolder=args.outfolder)
        return
