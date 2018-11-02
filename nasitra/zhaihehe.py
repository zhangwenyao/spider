#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from general import config as systemconfig

config = systemconfig.config


def zhaihehe(args):
    type = config['type']
    if not args.type:
        args.type = 'day'
    if args.type not in type:
        print("Type has to be set properly with -t/--type.")
        print('Valid List:\n\t', type)
        return

    if args.type == 'dailyCrawl':
        from zhaihehe.dailyCrawl import crawl
        return crawl()

    if not args.list:
        args.list = '8'
    if args.list not in config['list'].keys() \
       and args.list not in config['list'].values():
        print("List has to be set properly with -l/--list.")
        print('Valid List:\n\t', config['lists'])
        return

    if args.type in ('d', 'day', 'w', 'week', 'm', 'month', 'o', 'other'):
        if args.type == 'other' and not args.date2:
            print("Date2 has to be set properly with -2/--date2.")
            return
        if args.date and len(args.date) != 8:
            print("Date has to be set properly in '20170101' form.")
            return
        if args.date2 and len(args.date2) != 8:
            print("Date2 has to be set properly in '20170101' form.")
            return
        from zhaihehe.lists import crawl
        crawl(list=args.list, date=args.date, type=args.type,
              date2=args.date2, outfolder=args.outfolder)
        return

    if not args.date:
        args.date = (datetime.datetime.today() -
                     datetime.timedelta(days=1)).strftime("%Y%m%d")

    if args.type in ('a', 'analysis'):
        from zhaihehe.analysis import analysis
        analysis(list=args.list, listname=args.listname, infolder=args.infolder,
                 outfile=args.outfile, outfolder=args.outfolder)
        return

    if args.type == 'anchor':
        if not args.city:
            args.city = '0'
        if args.city not in config['city'].keys() \
           and args.city not in config['city'].values():
            print("City has to be set properly with --city.")
            print('Valid City:\n\t', config['city'])
            return
        if not args.sex:
            args.sex = '0'
        if args.sex not in config['sex'].keys() \
           and args.sex not in config['sex'].values():
            print("Sex has to be set properly with --sex.")
            print('Valid Sex:\n\t', config['sex'])
            return
        if not args.fans:
            args.fans = '0'
        if args.fans not in config['fans'].keys() \
           and args.fans not in config['fans'].values():
            print("Fans has to be set properly with --fans.")
            print('Valid Fans:\n\t', config['fans'])
            return
        from zhaihehe.anchor import crawl
        return crawl(date=args.date, list=args.list, city=args.city,
                     sex=args.sex, fans=args.fans, outfolder=args.outfolder,
                     range1=args.range1, range2=args.range2)

    if args.type == 'momoIds':
        from zhaihehe.anchor import momoIds
        return momoIds(infolder=args.infolder, outfolder=args.outfolder)

    if args.type == 'graph':
        from zhaihehe.graph import graph
        return graph(li=args.list, rankType=args.rankType)

    print('Type error:', args.type)
    return
