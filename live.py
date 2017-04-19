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
    parser.add_argument('--city', nargs='?', default='0',
                        help="specify the city which will be operated on.")
    parser.add_argument('--sex', nargs='?', default='0',
                        help="specify the sex which will be operated on.")
    parser.add_argument('--fans', nargs='?', default='0',
                        help="specify the fans which will be operated on.")
    parser.add_argument('--range1', nargs='?', default='0',
                        help="specify the range1 which will be operated on.")
    parser.add_argument('--range2', nargs='?', default='0',
                        help="specify the range2 which will be operated on.")
    parser.add_argument('params', nargs='*',
                        help='Different from action to action.')

    if len(argv) <= 1:
        parser.print_help()
        return None
    return parser.parse_args(argv)

import json
from general import config as sc


def main_load_config(args):
    data = json.load(args.config)
    sc.config = data.copy()

import sys


def main(argv=sys.argv[1:]):
    args = main_parser(argv)
    if args is None:
        return

    main_load_config(args)

    if args.list is None \
       or (args.list not in sc.config['list'].keys()
            and args.list not in sc.config['list'].values()):
        print("List has to be set properly with -l/--list.")
        print('Valid List:\n\t', sc.config['lists'])
        return None

    type = ['d', 'day', 'w', 'week', 'm', 'month', 'o', 'other',
            'a', 'analysis', 'anchor']
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

    if args.type in ('anchor'):
        if args.city is None \
           or (args.city not in sc.config['city'].keys()
                and args.city not in sc.config['city'].values()):
            print("City has to be set properly with --city.")
            print('Valid City:\n\t', sc.config['city'])
            return None
        if args.sex is None \
           or (args.sex not in sc.config['sex'].keys()
                and args.sex not in sc.config['sex'].values()):
            print("Sex has to be set properly with --sex.")
            print('Valid Sex:\n\t', sc.config['sex'])
            return None
        if args.fans is None \
           or (args.city not in sc.config['fans'].keys()
                and args.fans not in sc.config['fans'].values()):
            print("Fans has to be set properly with --fans.")
            print('Valid Fans:\n\t', sc.config['fans'])
            return None
        from general.anchor import anchor
        anchor(outfile=args.outfile, list=args.list, city=args.city,
               sex=args.sex, fans=args.fans, outfolder=args.outfolder,
               range1=args.range1, range2=args.range2)
        return None

    return None

if __name__ == "__main__":
    main()
