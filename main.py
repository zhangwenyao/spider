# -*- coding: utf-8 -*-


import sys
import json
import argparse
from general import config as systemconfig


def main_parser(argv):
    parser = argparse.ArgumentParser(
        prog='py live.py', description='crawl live data of zhaihehe.com')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s 2.0')
    parser.add_argument('-w', '--web', nargs='?', default='zhaihehe',
                        help='specify the web to crawl.')
    parser.add_argument('-c', '--config', nargs='?',
                        help='specify the configuration file.')
    parser.add_argument('-t', '--type', nargs='?',
                        help="specify the type which will be operated on.")
    parser.add_argument('-l', '--list', nargs='?',
                        help="specify the list which will be operated on.")
    parser.add_argument('--listname', nargs='?', default='0',
                        help="specify the listname which will be operated on.")
    parser.add_argument('-i', '--infile', nargs='?',
                        help="specify the filename of the input file.")
    parser.add_argument('--infolder', nargs='?',
                        help="specify the folder to import data.")
    parser.add_argument('-o', '--outfile', nargs='?',
                        help="specify the filename of the output file.")
    parser.add_argument('--outfolder', nargs='?',
                        help="specify where to save the output file in data/${list}.")
    parser.add_argument('-d', '--date', nargs='?',
                        help="specify the date in '20170101' form.")
    parser.add_argument('-2', '--date2', nargs='?',
                        help="specify the date in '20170101' form.")
    parser.add_argument('--rankType', nargs='?',
                        help="specify the rankType which will be operated on.")
    parser.add_argument('--dateType', nargs='?',
                        help="specify the dateType which will be operated on.")
    parser.add_argument('--city', nargs='?',
                        help="specify the city which will be operated on.")
    parser.add_argument('--sex', nargs='?',
                        help="specify the sex which will be operated on.")
    parser.add_argument('--fans', nargs='?',
                        help="specify the fans which will be operated on.")
    parser.add_argument('--range1', nargs='?',
                        help="specify the range1 which will be operated on.")
    parser.add_argument('--range2', nargs='?',
                        help="specify the range2 which will be operated on.")
    parser.add_argument('params', nargs='*',
                        help='Different from action to action.')

    if len(argv) < 1:
        parser.print_help()
        return None
    return parser.parse_args(argv)


def main_load_config(args):
    with open(args.config, 'r') as f:
        systemconfig.config.update(json.load(f))
    return


def main(argv=sys.argv[1:]):
    args = main_parser(argv)
    if args is None:
        return
    systemconfig.config = {"args":  args}

    web = ('z', 'zhaihehe', 't', 'talkingdata', 'b', 'baidu')
    if args.web not in web:
        print("Web has to be set properly with -w/--web.")
        print('Web List:\n\t', web)
        return

    if args.web in ('z', 'zhaihehe'):
        args.web = 'zhaihehe'
        if not args.config:
            args.config = 'config/zhaihehe.json'
        main_load_config(args)
        from nasitra.zhaihehe import zhaihehe
        return zhaihehe(args)

    if args.web in ('t', 'talkingdata'):
        args.web = 'talkingdata'
        if not args.config:
            args.config = 'config/talkingdata.json'
        main_load_config(args)
        from nasitra.talkingdata import talkingdata
        return talkingdata(args)

    if args.web in ('baiduMOTA'):
        args.web = 'baiduMOTA'
        if not args.config:
            args.config = 'config/baiduMOTA.json'
        main_load_config(args)
        from nasitra.baiduMOTA import baiduMOTA
        return baiduMOTA(args)


if __name__ == "__main__":
    main()
