#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import subprocess
from datetime import datetime, timedelta
from general import config as systemconfig

config = systemconfig.config


def graph(rankType=None, li=None):
    if not rankType:
        rankType = 'detailRank'
    if not li:
        li = config['list']

    if rankType == 'detailRank':
        detailRank_static(li)
        detailRank_graph(li)

    if rankType == 'index':
        index_static(li)
        index_graph(li)


def detailRank_static(li):
    # detailinfo
    fld = os.path.join('data', config['args'].web, li)
    key = '-detailinfo.txt'
    files = [x for x in os.listdir(fld)
             if x.endswith(key) and os.path.isfile(os.path.join(fld, x))]
    if not files:
        logging.info('data is empty.')
        return
    dates = [x[0:6] for x in files]
    dates.sort()

    outFld = os.path.join('export', config['args'].web, li)
    filename = os.path.join(
        outFld, '{}-{}-detailRank.txt'.format(dates[0], dates[-1]))
    if os.path.exists(filename):
        return
    if not os.path.exists(outFld):
        os.makedirs(outFld)

    data = {}
    for d in dates:
        data[d] = {}
        flagAll = False
        flagCate = False
        with open(os.path.join(fld, d + key), 'r') as f:
            for l in f.readlines():
                l = l.strip().split('\t')
                if l[0] == 'rank_all_inst':
                    data[d]['all'] = int(l[1])
                    flagAll = True
                elif l[0] == 'rank_cate_inst':
                    data[d]['cate'] = int(l[1])
                    flagCate = True
                if flagAll and flagCate:
                    break
        if not flagAll or not flagCate:
            logging.info('data error: ' + d)
            return

    with open(filename, 'w') as f:
        f.write('#date\tall\tcate\n')
        for d in dates:
            f.write('{}\t{}\t{}\n'.format(d, data[d]['all'], data[d]['cate']))
    logging.info('save file: ' + filename)


def detailRank_graph(li):
    # detailinfo
    fld = os.path.join('export', config['args'].web, li)
    key = '-detailRank.txt'
    files = [x for x in os.listdir(fld)
             if x.endswith(key) and os.path.isfile(os.path.join(fld, x))]
    files.sort()
    if not files:
        logging.info('data is empty')
        return
    filename = files[-1]
    infile = os.path.join(fld, filename)
    outfile = infile[0:-4]
    if os.path.exists(outfile + 'All.eps') \
       and os.path.exists(outfile + 'All.pdf') \
       and os.path.exists(outfile + 'Cate.eps') \
       and os.path.exists(outfile + 'Cate.pdf'):
        return

    try:
        code = 0
        sh = os.path.join('script', 'gnuplot_eps_pdf.sh')
        plt = os.path.join(config['args'].web, 'detailRankAll.plt')
        outfile2 = outfile + 'All'
        cmd = '{} {} {} \\"{}\\"'.format(sh, plt, outfile2, infile)
        out_bytes = subprocess.check_output(cmd, stderr=subprocess.STDOUT,
                                            shell=True)
        logging.info('save files: ' + outfile2)
        plt = os.path.join(config['args'].web, 'detailRankCate.plt')
        outfile2 = outfile + 'Cate'
        cmd = '{} {} {} \\"{}\\"'.format(sh, plt, outfile2, infile)
        out_bytes = subprocess.check_output(cmd, stderr=subprocess.STDOUT,
                                            shell=True)
        logging.info('save files: ' + outfile2)
    except subprocess.CalledProcessError as e:
        out_bytes = e.output
        code = e.returncode
        # logging.info('graph error')
        logging.info('graph error')
        return code, out_bytes


def index_static(li):
    # detailinfo
    fld = os.path.join('data', config['args'].web, li)
    key = '-index.txt'
    files = [x for x in os.listdir(fld)
             if x.endswith(key) and os.path.isfile(os.path.join(fld, x))]
    if not files:
        logging.info('data is empty.')
        return
    files.sort()
    file = files[-1]
    date = file[:8]
    d = datetime.strptime(date, '%Y%m%d')
    date2 = file[9:17]
    d2 = datetime.strptime(date2, '%Y%m%d')

    outFld = os.path.join('export', config['args'].web, li)
    filename = os.path.join(
        outFld, '{}-{}-index.txt'.format(date, date2))
    if os.path.exists(filename):
        return
    if not os.path.exists(outFld):
        os.makedirs(outFld)

    with open(os.path.join(fld, file), 'r') as f:
        datas = f.readlines()
    if len(datas) != (d2 - d).days + 1:
        print('data error')
    dd = d
    with open(os.path.join(filename), 'w') as f:
        f.write('#date\tindex\n')
        for v in datas:
            f.write('{}\t{}\n'.format(dd.strftime('%Y%m%d'), v.strip()))
            dd += timedelta(days=1)
    print('save file: ' + filename)


def index_graph(li):
    # detailinfo
    fld = os.path.join('export', config['args'].web, li)
    key = '-index.txt'
    files = [x for x in os.listdir(fld)
             if x.endswith(key) and os.path.isfile(os.path.join(fld, x))]
    files.sort()
    if not files:
        logging.info('data is empty')
        return
    filename = files[-1]
    infile = os.path.join(fld, filename)
    outfile = infile[0:-4]
    if os.path.exists(outfile + '.eps') and os.path.exists(outfile + '.pdf'):
        return

    try:
        code = 0
        sh = os.path.join('script', 'gnuplot_eps_pdf.sh')
        plt = os.path.join(config['args'].web, 'index.plt')
        cmd = '{} {} {} \\"{}\\"'.format(sh, plt, outfile, infile)
        out_bytes = subprocess.check_output(cmd, stderr=subprocess.STDOUT,
                                            shell=True)
        logging.info('save files: ' + outfile)
    except subprocess.CalledProcessError as e:
        out_bytes = e.output
        code = e.returncode
        # logging.info('graph error')
        logging.info('graph error')
        return code, out_bytes
