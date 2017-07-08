#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import csv
import logging
import subprocess
from general import config as systemconfig

config = systemconfig.config


def graph(li=None, rankType=None):
    if not li:
        li = '8'
    if not rankType:
        rankType = 'day'

    data_static(li, rankType)
    data_graph(li, rankType)


def data_static(li, rankType):
    infld = os.path.join('data', config['args'].web, li, rankType)
    key = '.csv'
    files = [x for x in os.listdir(infld)
             if x.endswith(key)
             and os.path.isfile(os.path.join(infld, x))
             and os.path.getsize(os.path.join(infld, x)) > 500]
    if not files:
        logging.info('files is empty')
        return
    files.sort()

    means = []
    for x in files:
        s = 0
        l = 0
        with open(os.path.join(infld, x), 'r') as f:
            f_csv = csv.DictReader(f)
            for r in f_csv:
                if '虚拟币' not in r:
                    logging.info('虚拟币 not in file error: ' + x)
                    return
                v = int(r['虚拟币'])
                if v < 10000:
                    logging.debug('虚拟币 < 10000:\t{}\t{}\t{}'.format(v, x, r))
                    break
                s += v
                l += 1
        if l != 20:
            logging.debug('data length != 20 error:\t{}\t{}'.format(l, x))
            continue
        means.append([x[0:8], s / 20.0])

    if not means:
        logging.info('data is empty')
        return
    fld = os.path.join('export', config['args'].web, li)
    filename = os.path.join(fld, '{}-{}-{}-means.txt'.format(
        means[0][0], means[-1][0], rankType))
    if os.path.exists(filename):
        return
    if not os.path.exists(fld):
        os.makedirs(fld)

    with open(filename, 'w') as f:
        f.write('#date\tmean\n')
        for x in means:
            f.write('{}\t{}\n'.format(x[0], x[1]))
    logging.info('save file: ' + filename)


def data_graph(li, rankType):
    fld = os.path.join('export', config['args'].web, li)
    key = '-{}-means.txt'.format(rankType)
    files = [x for x in os.listdir(fld)
             if x.endswith(key)
             and os.path.isfile(os.path.join(fld, x))
             and len(x) == 8 + 1 + 8 + len(key)]
    if not files:
        logging.info('data files are empty')
        return
    files.sort()
    infile = os.path.join(fld, files[-1])
    outfile = infile[:-4]
    if os.path.exists(outfile + '.eps'):
        return

    try:
        # code = 0
        sh = os.path.join('script', 'gnuplot_eps_pdf.sh')
        plt = os.path.join('config', config['args'].web,
                           '{}-means.plt'.format(rankType))
        cmd = '{} {} {} \\"{}\\"'.format(sh, plt, outfile, infile)
        out_bytes = subprocess.check_output(cmd, stderr=subprocess.STDOUT,
                                            shell=True)
        logging.info('save files: ' + outfile)
    except subprocess.CalledProcessError as e:
        out_bytes = e.output
        # code = e.returncode
        # return code, out_bytes
        logging.info('graph error')
        logging.debug(out_bytes)
