#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
from datetime import datetime
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

    if rankType == 'rankStarHour2':
        # rankStarHour2_static()
        rankStarHour2_day_graph()


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
    outfiles = [x for x in os.listdir(outfld)
                if os.path.isfile(os.path.join(outfld, x))
                and x.endswith('.txt')
                and len(x) == 13 + 1 + 13 + 4]
    if outfiles:
        outfiles.sort()
        time1 = outfiles[-1][:13]
        time2 = outfiles[-1][14:27]
        if time1 > files[0][:13]:
            time1 = files[0][:13]

        if time2 < files[-1][:13]:
            time2 = files[-1][:13]

    else:
        time1 = files[0][:13]
        time2 = files[-1][:13]

    filename = os.path.join(outfld, '{}_{}.txt'.format(time1, time2))
    if os.path.exists(filename):
        return

    means = {}
    if outfiles:
        with open(os.path.join(outfld, outfiles[-1]), 'r') as f:
            d = f.readlines()

        d = [x.strip().split() for x in d[1:]]
        for x in d:
            means[x[0]] = x[1]

    for x in files:
        if x[:13] in means:
            continue

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

            else:
                i = float(i)

            s += i

        s /= len(d)
        means[x[:13]] = str(s)

    keys = list(means.keys())
    keys.sort()
    with open(filename, 'w') as f:
        f.write('#time\tmean\n')
        for x in keys:
            f.write('{}\t{}\n'.format(x, means[x]))

    logging.info('save file: ' + filename)

    outfiles = [x for x in os.listdir(outfld)
                if os.path.isfile(os.path.join(outfld, x))
                and x.endswith('.txt')
                and len(x) == 8 + 1 + 8 + 4]
    if outfiles:
        outfiles.sort()
        date1 = outfiles[-1][:8]
        date2 = outfiles[-1][9:17]
        if date1 > files[0][:8]:
            date1 = files[0][:8]

        if date2 < files[-1][:8]:
            date2 = files[-1][:8]

    else:
        date1 = files[0][:8]
        date2 = files[-1][:8]

    filename = os.path.join(outfld, '{}_{}.txt'.format(date1, date2))

    if os.path.exists(filename):
        return

    datas = {}
    for x in means:
        date = x[0:8]
        if date not in datas:
            datas[date] = []

        datas[date].append(means[x])

    dates = list(datas.keys())
    dates.sort()
    del dates[-1]
    filename = os.path.join(outfld, '{}_{}.txt'.format(dates[0], dates[-1]))
    if os.path.exists(filename):
        return

    with open(filename, 'w') as f:
        f.write('#date\tmean\n')
        for date in dates:
            s = 0.0
            for x in datas[date]:
                s += float(x)

            f.write('{}\t{}\n'.format(date, s / len(datas[date]) * 24))

    logging.info('save file: ' + filename)


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


def rankStarHour2_static():
    infld = os.path.join('data', config['args'].web, 'rank', 'star_hour2')
    files = [x for x in os.listdir(infld)
             if os.path.isfile(os.path.join(infld, x))
             and os.path.getsize(os.path.join(infld, x)) > 500
             and len(x) == 17]
    if not files:
        logging.info('data is empty')
        return

    files.sort()

    outfld = os.path.join('export', config['args'].web, 'rankStarHour2')
    if not os.path.exists(outfld):
        os.makedirs(outfld)

    outfiles = [x for x in os.listdir(outfld)
                if os.path.isfile(os.path.join(outfld, x))
                and x.endswith('.txt')
                and len(x) == 8 + 1 + 8 + 4]
    if outfiles:
        outfiles.sort()

    means = {}
    hours = {}
    if outfiles:
        with open(os.path.join(outfld, outfiles[-1]), 'r') as f:
            d = f.readlines()

        if len(d) > 1:
            d = [x.strip().split() for x in d[1:]]
            for x in d:
                means[x[0]] = x[1]
                hours[x[0]] = x[2]

    means2 = {}
    for x in files:
        if x[:8] in means:
            continue

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

            else:
                i = float(i)

            s += i

        s /= len(d)
        day = x[:8]
        hour = x[9:11]
        if day not in means2:
            means2[day] = {}

        if hour not in means2[day]:
            means2[day][hour] = 0

        if s > means2[day][hour]:
            means2[day][hour] = s

    keys2 = list(means2.keys())
    keys2.sort()
    keys = list(means.keys())
    keys.sort()
    if len(keys) <= 0 or keys2[-1] > keys[-1]:
        del keys2[-1]

    if len(keys2) <= 0:
        logging.info('data is empty')
        return

    for day in keys2:
        m = 0
        for star in means2[day].values():
            m += star

        hours[day] = len(means2[day])
        means[day] = m / hours[day] * 24

    keys = list(means.keys())
    keys.sort()
    filename = os.path.join(outfld, '{}_{}.txt'.format(keys[0], keys[-1]))
    with open(filename, 'w') as f:
        f.write('#time\tday_mean\thours\n')
        for x in keys:
            f.write('{}\t{}\t{}\n'.format(x, means[x], hours[x]))

    logging.info('save file: ' + filename)


def rankStarHour2_day_graph():
    fld = os.path.join('export', config['args'].web, 'rankStarHour2')
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
    if not os.path.exists(outfile + '.png'):
        try:
            # code = 0
            sh = os.path.join('script', 'gnuplot_png_pdf.sh')
            plt = os.path.join(
                'config', config['args'].web, 'rankStarHour2-day.plt')
            cmd = '{} {} {} \\"{}\\"'.format(sh, plt, outfile, infile)
            out_bytes = subprocess.check_output(cmd, stderr=subprocess.STDOUT,
                                                shell=True)
            logging.info('save files: ' + outfile)
            now = datetime.now()
            if now.isoweekday() == 5:
                send_email(infile[-12:-4], outfile + '.png')

        except subprocess.CalledProcessError as e:
            out_bytes = e.output
            # code = e.returncode
            # return code, out_bytes
            logging.info('graph error')
            logging.debug(out_bytes)

    outfile = infile[:-4] + '-log'
    if not os.path.exists(outfile + '.png'):
        try:
            # code = 0
            sh = os.path.join('script', 'gnuplot_png_pdf.sh')
            plt = os.path.join(
                'config', config['args'].web, 'rankStarHour2-day-log.plt')
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


import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


def send_email(date, img):
    gmail_config = config['logconfig']['handlers']['gmail']
    username = gmail_config['credentials'][0]
    password = gmail_config['credentials'][1]
    smtp_server = gmail_config['mailhost'][0]
    smtp_port = gmail_config['mailhost'][1]
    from_addr = gmail_config['fromaddr']
    to_addrs = ['zinppy@gmail.com']
    cc_addrs = gmail_config['toaddrs']

    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = ', '.join(to_addrs)
    msg['Cc'] = ', '.join(cc_addrs)
    msg['Subject'] = Header('陌陌的星光值数据 %s' % date, 'utf-8').encode()
    msg.attach(MIMEText(
        '<html><body><h2>陌陌榜单用户最新的收入星光值数据图</h2>' + '<p><img src="cid:0"></p>'
        + '</body></html>', 'html', 'utf-8'))
    with open(img, 'rb') as f:
        mime = MIMEImage(f.read())
        mime.add_header('Content-Disposition', 'attachment', filename=img)
        mime.add_header('Content-ID', '<0>')
        mime.add_header('X-Attachment-Id', '0')
        msg.attach(mime)

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    # server.set_debuglevel(1)
    server.login(username, password)
    server.sendmail(from_addr, to_addrs + cc_addrs, msg.as_string())
    server.quit()
    return
