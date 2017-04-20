#!/usr/bin/env python
# -*- coding: utf-8 -*-


def talkingdata(args):

    type = ('app', 'appStore')
    if not args.type:
        args.type = 'app'
    if args.type not in type:
        print("Type has to be set properly with -t/--type.")
        print('Valid List:\n\t', type)
        return

    if args.type in ('app'):
        from talkingdata.app import crawl
        return crawl(args)

    print('Type error:', args.type)
    return
