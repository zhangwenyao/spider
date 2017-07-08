#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import subprocess
from general import config as systemconfig

config = systemconfig.config


def graph(rankType=None, dateType=None):
    rankTypes = config['type']['rank']['rankType']
    if rankType == 'all':
        rankType = rankTypes
    elif rankType in rankTypes:
        rankType = [rankType]
    else:
        rankTypes.append('all')
        logging.info("RankType has to be set properly with --rankType.")
        logging.info('Valid List:\n\t{}'.format(rankTypes))
        return

    dateTypes = list(config['type']['rank']['dateType'])
    if dateType == 'all':
        dateType = dateTypes
    elif dateType in dateTypes:
        dateType = [dateType]
    else:
        dateTypes.append('all')
        logging.info("DateType has to be set properly with --dateType.")
        logging.info('Valid List:\n\t{}'.format(dateTypes))
        return

    for r in rankType:
        for d in dateType:
            rank_static(rankType=r, dateType=d)
            rank_graph(rankType=r, dateType=d)


def rank_static(rankType, dateType):
    # detailinfo
    inFld = os.path.join('data', config['args'].web, 'rank',
                         rankType + '-' + dateType)
    files = [x for x in os.listdir(inFld)
             if os.path.isfile(os.path.join(inFld, x))
             and x.endswith('.txt') and len(x) == 13 + 4]
    if not files:
        logging.info('data is empty.')
        return
    files.sort()
    date1 = files[0][0:8]
    date2 = files[-1][0:8]

    outFld = os.path.join('export', config['args'].web)
    key = '-{}-{}.txt'.format(rankType, dateType)
    outfiles = [x for x in os.listdir(outFld)
                if os .path.isfile(os.path.join(outFld, x))
                and x.endswith(key) and len(x) == 8 + 1 + 8 + len(key)]
    if outfiles:
        outfiles.sort()
        date1 = outfiles[-1][0:8]
    filename = os.path.join(outFld, '{}-{}{}'.format(date1, date2, key))
    if os.path.exists(filename):
        return
    if not os.path.exists(outFld):
        os.makedirs(outFld)

    means = []
    if outfiles:
        with open(os.path.join(outFld, outfiles[-1]), 'r') as f:
            lines = f.readlines()
        for l in lines[1:]:
            l = l.strip().split('\t')
            means.append([l[0], l[1]])
            infilename = l[0] + '.txt'
            if infilename in files:
                files.remove(infilename)
    if not files:
        return

    for d in files:
        with open(os.path.join(inFld, d), 'r') as f:
            datas = f.readlines()
        datas = [x.split('\t') for x in datas]
        if len(datas) != 31:
            logging.info('file length != 31 error: ' + d)
            means.append(['#' + d[0:13], -1])
            continue
        if 'cnt' not in datas[0]:
            logging.info('data does not have "cnt" error: ' + datas[0])
            continue
        index = datas[0].index('cnt')
        s = 0
        for i in datas[1:]:
            s += int(i[index])
        means.append([d[0:13], s / (len(datas) - 1)])

    with open(filename, 'w') as f:
        f.write('#time\tmean\n')
        for m in means:
            f.write('{}\t{}\n'.format(m[0], m[1]))
    logging.info('save file: ' + filename)


def rank_graph(rankType, dateType):
    fld = os.path.join('export', config['args'].web)
    key = '-{}-{}.txt'.format(rankType, dateType)
    files = [x for x in os.listdir(fld)
             if x.endswith(key) and os.path.isfile(os.path.join(fld, x))
             and len(x) == 8 + 1 + 8 + len(key)]
    if not files:
        logging.info('data is empty: {} {}'.format(rankType, dateType))
        return
    files.sort()
    infile = os.path.join(fld, files[-1])
    outfile = infile[0:-4]
    if os.path.exists(outfile + '.eps'):
        return

    try:
        # code = 0
        sh = os.path.join('script', 'gnuplot_eps_pdf.sh')
        plt = os.path.join('config', config['args'].web,
                           '{}-{}.plt'.format(rankType, dateType))
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
