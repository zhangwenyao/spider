#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import subprocess
from general import config as systemconfig

config = systemconfig.config


def graph(rankType=None):
    if not rankType:
        rankType = 'starDay'

    if rankType == 'starDay':
        starDay_static()
        starDay_graph()

    if rankType == 'rankStarHour':
        rankStarHour_static()
        rankStarHour_graph()
        rankStarHour_day_graph()


def starDay_static():
    fld = os.path.join('export', config['args'].web)
    key = 'star-day-join'
    files = [x for x in os.listdir(fld)
             if x.startswith(key)
             and os.path.isfile(os.path.join(fld, x))
             and os.path.getsize(os.path.join(fld, x)) > 2000
             and len(x) == len(key) + 1 + 8 + 1 + 8 + 4]
    if not files:
        logging.info('data is empty.')
        return
    files.sort()
    infile = os.path.join(fld, files[-1])

    filename = os.path.join(fld, files[-1][:-4] + '-means.txt')
    if os.path.exists(filename):
        return

    with open(infile, 'r') as f:
        data = f.readlines()
    # ids = data[0].strip()
    data = data[2:]
    data = [x.strip().split() for x in data]
    if not data:
        logging.info('data is empty: ' + infile)
        return
    n = len(data[0])
    if n <= 1:
        logging.info('data error, length <= 1: ' + data[0])
        return
    means = []
    for x in data:
        if len(x) != n:
            logging.info('data length error: ' + x)
            return
        s = 0
        for i in x[1:]:
            s += int(i)
        means.append([x[0], s / (n - 1.0)])

    with open(filename, 'w') as f:
        f.write('#date\tmean\n')
        for x in means:
            f.write('{}\t{}\n'.format(x[0], x[1]))
    logging.info('save file: ' + filename)


def starDay_graph():
    fld = os.path.join('export', config['args'].web)
    files = [x for x in os.listdir(fld)
             if x.startswith('star-day-join-')
             and x.endswith('-means.txt')
             and os.path.isfile(os.path.join(fld, x))]
    if not files:
        logging.info('data is empty')
        return
    files.sort()
    infile = os.path.join(fld, files[-1])
    outfile = infile[:-4]
    if os.path.exists(outfile + '.eps'):
        return

    try:
        # code = 0
        sh = os.path.join('script', 'gnuplot_eps_pdf.sh')
        plt = os.path.join('config', config['args'].web, 'star-day-means.plt')
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


def rankStarHour_static():
    infld = os.path.join('data', config['args'].web, 'rank', 'star_hour')
    files = [x for x in os.listdir(infld)
             if os.path.isfile(os.path.join(infld, x))
             and os.path.getsize(os.path.join(infld, x)) > 500
             and len(x) == 17]
    if not files:
        logging.info('data is empty.')
        return
    files.sort()

    outfld = os.path.join('export', config['args'].web, 'rankStarHour')
    filename = os.path.join(outfld, '{}_{}.txt'.format(
        files[0][:13], files[-1][:13]))
    if os.path.exists(filename):
        return

    means = []
    for x in files:
        with open(os.path.join(infld, x), 'r') as f:
            d = f.readlines()
        head = d[0]
        head = head.strip().split()
        if 'hour_thumb' not in head:
            logging.info('hour_thumb not in headers error: ' + x)
            continue
        index = head.index('hour_thumb')
        d = d[1:]
        if len(d) != 50:
            logging.debug('length != 50 error: ' + x)
            continue
        d = [x.strip().split() for x in d]
        d = [x[index] for x in d]
        s = 0.0
        for i in d:
            if '亿' in i:
                i = i.replace('亿', '')
                i = float(i) * 100000000
            elif '千万' in i:
                i = i.replace('千万', '')
                i = float(i) * 10000000
            elif '万' in i:
                i = i.replace('万', '')
                i = float(i) * 10000
            # elif '千' in i:
                # i = i.replace('千', '')
                # i = float(i) * 1000
            else:
                i = float(i)
            s += i
        s /= len(d)
        means.append([x[:13], s])

    with open(filename, 'w') as f:
        f.write('#time\tmean\n')
        for x in means:
            f.write('{}\t{}\n'.format(x[0], x[1]))
    logging.info('save file: ' + filename)

    datas = {}
    for x in means:
        date = x[0][0:8]
        if date not in datas:
            datas[date] = []
        datas[date].append(x[1])
    dates = list(datas.keys())
    dates.sort()
    del dates[-1]
    filename2 = os.path.join(outfld, '{}_{}.txt'.format(
        dates[0], dates[-1]))
    if os.path.exists(filename2):
        return
    with open(filename2, 'w') as f:
        f.write('#date\tmean\n')
        for date in dates:
            s = 0.0
            for x in datas[date]:
                s += x
            f.write('{}\t{}\n'.format(date, s / len(datas[date]) * 24))


def rankStarHour_graph():
    fld = os.path.join('export', config['args'].web, 'rankStarHour')
    files = [x for x in os.listdir(fld)
             if x.endswith('.txt')
             and os.path.isfile(os.path.join(fld, x))
             and len(x) == 13 + 1 + 13 + 4]
    if not files:
        logging.info('data is empty')
        return
    files.sort()
    infile = os.path.join(fld, files[-1])
    outfile = infile[:-4]
    if os.path.exists(outfile + '.eps'):
        return

    try:
        # code = 0
        sh = os.path.join('script', 'gnuplot_eps_pdf.sh')
        plt = os.path.join('config', config['args'].web, 'rankStarHour.plt')
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


def rankStarHour_day_graph():
    fld = os.path.join('export', config['args'].web, 'rankStarHour')
    files = [x for x in os.listdir(fld)
             if x.endswith('.txt')
             and os.path.isfile(os.path.join(fld, x))
             and len(x) == 8 + 1 + 8 + 4]
    if not files:
        logging.info('data is empty')
        return
    files.sort()
    infile = os.path.join(fld, files[-1])

    outfile = infile[:-4]
    if not os.path.exists(outfile + '.eps'):
        try:
            # code = 0
            sh = os.path.join('script', 'gnuplot_eps_pdf.sh')
            plt = os.path.join(
                'config', config['args'].web, 'rankStarHour-day.plt')
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

    outfile = infile[:-4] + '-log'
    if not os.path.exists(outfile + '.eps'):
        try:
            # code = 0
            sh = os.path.join('script', 'gnuplot_eps_pdf.sh')
            plt = os.path.join(
                'config', config['args'].web, 'rankStarHour-day-log.plt')
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
