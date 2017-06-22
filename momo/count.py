import os
import logging
from datetime import datetime, timedelta


def day(date1=None, date2=None):
    if not date1:
        date1 = '20170513'
    ti1 = datetime.strptime(date1, '%Y%m%d')
    if not date2:
        date2 = datetime.strftime(
            datetime.utcnow() + timedelta(hours=8), '%Y%m%d')
    ti2 = datetime.strptime(date2, '%Y%m%d')
    date3 = (ti2 - timedelta(days=1)).strftime('%Y%m%d')

    infile = os.path.join('infiles', 'momo-ids.txt')
    with open(infile, 'r') as f:
        ids = f.read().split()
    star = {}
    for id in ids:
        outFld = os.path.join('export', 'momo', 'star-day')
        outfile = os.path.join(outFld, '{}-{}-{}.txt'.format(id, date1, date3))
        if os.path.exists(outfile):
            continue
        if not os.path.exists(outFld):
            os.makedirs(outFld)

        star = []
        infile = os.path.join('data', 'momo', 'star', id + '.txt')
        logging.info('read file: ' + infile)
        n = 0
        dayStar = 0
        d = date1
        ti = ti1
        with open(infile, 'r') as f:
            for i in f:
                data = i.split()
                time = datetime.strptime(data[0], '%Y%m%d-%H%M%S')
                s = data[1]
                if s.find('万') >= 0 or s.find('亿') >= 0:
                    if s.find('万') >= 0:
                        s = s.replace('万', '0000')
                        s = int(s)
                        if n - 10000 < s <= n - n % 10000:
                            s = n
                    elif s.find('亿') >= 0:
                        s = s.replace('亿', '00000000')
                        s = int(s)
                        if n - 100000000 < s <= n - n % 100000000:
                            s = n
                s = int(s)
                if time < ti:
                    logging.debug('skip data: ' + data)
                    continue
                if time >= ti2:
                    break
                if s <= 0:
                    if n <= 0 and d == data[0][0:8]:
                        ti = time
                    continue
                # renewing
                if data[0][0:8] != d or s < n or time >= ti + timedelta(hours=6):
                    if s >= n and ti + timedelta(hours=3) <= time:
                        logging.debug('  long interval:', data,
                                      datetime.strftime(ti, '%Y%m%d-%H%M%S'), n)
                    dayStar += n
                    if data[0][0:8] != d:
                        star.append('\t'.join([d, str(dayStar)]))
                        if s < n or time >= ti + timedelta(hours=6):
                            dayStar = 0
                        else:
                            dayStar = -n
                        d = datetime.strftime(ti + timedelta(days=1), '%Y%m%d')
                        ti = datetime.strptime(d, '%Y%m%d')
                        while d != data[0][0:8] and ti <= time:
                            star.append('\t'.join([d, str(dayStar)]))
                            d = datetime.strftime(
                                ti + timedelta(days=1), '%Y%m%d')
                            ti = datetime.strptime(d, '%Y%m%d')
                n = s
                d = data[0][0:8]
                ti = time
        dayStar += n
        while d != date2 and ti < ti2:
            star.append('\t'.join([d, str(dayStar)]))
            dayStar = 0
            d = datetime.strftime(ti + timedelta(days=1), '%Y%m%d')
            ti = datetime.strptime(d, '%Y%m%d')

        with open(outfile, 'w') as f:
            f.write('#date\tstar\n')
            f.write('\n'.join(star))
        logging.info('save file: ' + outfile)


def time():
    infile = os.path.join('infiles', 'momo-ids.txt')
    with open(infile, 'r') as f:
        ids = f.read().split()
    for id in ids:
        star = []
        infile = os.path.join('data', 'momo', 'star',  id + '.txt')
        logging.info('read file: ' + infile)
        with open(infile, 'r') as f:
            n = 0
            t = None
            ti = None
            for i in f:
                data = i.split()
                time = datetime.strptime(data[0], '%Y%m%d-%H%M%S')
                s = data[1]
                if s.find('万') >= 0 or s.find('亿') >= 0:
                    if s.find('万') >= 0:
                        s = s.replace('万', '0000')
                        s = int(s)
                        if n - 10000 < s <= n - n % 10000:
                            logging.debug('{}\t{}\t{}'.format(data, t, n))
                            s = n
                    elif s.find('亿') >= 0:
                        s = s.replace('亿', '00000000')
                        s = int(s)
                        if n - 100000000 < s <= n - n % 100000000:
                            logging.debug('{}\t{}\t{}'.format(data, t, n))
                            s = n
                s = int(s)
                if n <= 0:
                    n = s
                    t = data[0]
                    ti = time
                    if s <= 0:
                        continue
                if s > 0:
                    if s < n or time >= ti + timedelta(hours=6):
                        star.append('\t'.join([t, str(n)]))
                        if s >= n and ti + timedelta(hours=3) <= time:
                            logging.debug('long interval: {}\t{}\t{}'.format(
                                data, t, n))
                    n = s
                    t = data[0]
                    ti = time
        if t:
            star.append('\t'.join([t, str(n)]))
        outFld = os.path.join('export', 'momo', 'star-time')
        if not os.path.exists(outFld):
            os.makedirs(outFld)
        outfile = os.path.join(outFld, id + '.txt')
        with open(outfile, 'w') as f:
            f.write('#day\tstar\n')
            f.write('\n'.join(star))
        logging.info('save file: ' + outfile)
