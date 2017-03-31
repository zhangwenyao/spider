# -*- coding: utf-8 -*-


import argparse


def main_parser(argv):
    parser = argparse.ArgumentParser(
        prog='py live.py', description='crawl live data of zhaihehe.com')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s 1.0')
    parser.add_argument('-c', '--config', nargs='?', default='config/api.json',
                        type=argparse.FileType('r'), help='specify the configuration file.')
    parser.add_argument('-l', '--list', nargs='?', default='4',
                        help="specify the list which will be operated on.")
    parser.add_argument('-o', '--outfolder', nargs='?', default='day',
                        help="specify where to save the output file in data/${list}.")
    parser.add_argument('-d', '--date', nargs='?', default='20170101',
                        help="specify the date in '20170101' form.")
    parser.add_argument('-2', '--date2', nargs='?',
                        help="specify the date in '20170101' form.")
    parser.add_argument('params', nargs='*',
                        help='Different from action to action.')

    if len(argv) <= 1:
        parser.print_help()
        return None
    return parser.parse_args(argv)

import json
from general import config as systemconfig


def main_load_config(args):
    data = json.load(args.config)
    systemconfig.api = data['api']
    systemconfig.lists = data['lists']

import sys


def main(argv=sys.argv[1:]):
    args = main_parser(argv)
    if args is None:
        return

    main_load_config(args)

    if args.list is None \
       or (args.list not in systemconfig.lists.keys()
            and args.list not in systemconfig.lists.values()):
        print("List has to be set properly with -l/--list.")
        print('Valid List:\n\t', systemconfig.lists)
        return None

    outfolder = ['day', 'week', 'month']
    if args.outfolder not in outfolder:
        print("Outfolder has to be set properly with -o/--outfolder.")
        print('Valid List:\n\t', outfolder)
        return None

    from general.spider import crawl
    crawl(list=args.list, outfolder=args.outfolder,
          date=args.date, d2=args.date2)

    return

if __name__ == "__main__":
    main()
