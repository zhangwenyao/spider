# -*- coding: utf-8 -*-


import argparse


def main_parser(argv):
    parser = argparse.ArgumentParser(
        prog='py live.py', description='crawl live data of zhaihehe.com')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s 1.0')
    parser.add_argument('-c', '--config', nargs='?', default='config/api.json',
                        type=argparse.FileType('r'), help='specify the configuration file.')
    parser.add_argument('-l', '--list', nargs='?', default='0',
                        help="specify the list which will be operated on.")
    parser.add_argument('-t', '--type', nargs='?', default='day',
                        help="specify the type which will be operated on.")
    parser.add_argument('--listname', nargs='?', default='0',
                        help="specify the listname which will be operated on.")
    parser.add_argument('-i', '--infolder', nargs='?',
                        help="specify the folder to import data.")
    parser.add_argument('-o', '--outfile', nargs='?',
                        help="specify the filename of the output file.")
    parser.add_argument('--outfolder', nargs='?',
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

    type = ['d', 'day', 'w', 'week', 'm', 'month', 'o', 'other',
            'a', 'analysis']
    if args.type not in type:
        print("Type has to be set properly with -y/--type.")
        print('Valid List:\n\t', type)
        return None

    if args.type in ('d', 'day', 'w', 'week', 'm', 'month', 'o', 'other'):
        if args.type == 'other' and not args.date2:
            print("Date2 has to be set properly with -2/--date2.")
            return None
        if len(args.date) != 8:
            print("Date has to be set properly in '20170101' form.")
            return None
        if args.date2 and len(args.date2) != 8:
            print("Date has to be set properly in '20170101' form.")
            return None
        from general.spider import crawl
        crawl(list=args.list, type=args.type, date=args.date,
              date2=args.date2, outfolder=args.outfolder)
        return None

    if args.type in ('a', 'analysis'):
        from general.analysis import analysis
        analysis(list=args.list, listname=args.listname, infolder=args.infolder,
                 outfile=args.outfile, outfolder=args.outfolder)
        return None

    return None

if __name__ == "__main__":
    main()
