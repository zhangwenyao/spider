import sys
from datetime import datetime, timedelta


def main(argv=sys.argv[1:]):
    date1 = '20170513'
    date2 = datetime.strftime(datetime.utcnow() + timedelta(hours=8), '%Y%m%d')
    if len(argv) > 0:
        if len(argv) != 2:
            print('ERROR: length of argv:', argv)
            return
        date1 = argv[0]
        date2 = argv[1]
    print(date1, date2)
    ti1 = datetime.strptime(date1, '%Y%m%d')
    ti2 = datetime.strptime(date2, '%Y%m%d')

    infile = "infiles/momo-ids.txt"
    with open(infile, 'r') as f:
        ids = f.read().split()
    star = {}
    for id in ids:
        star = []
        filename = 'data/momo/star/' + id + '.txt'
        print('read file:', filename)
        n = 0
        dayStar = 0
        d = date1
        ti = ti1
        with open(filename, 'r') as f:
            for i in f:
                data = i.split()
                time = datetime.strptime(data[0], '%Y%m%d-%H%M%S')
                s = int(data[1])
                if time < ti:
                    print('skip data:', data)
                    continue
                if s <= 0:
                    if n <= 0 and d == data[0][0:8]:
                        ti = time
                    continue
                # renewing
                if data[0][0:8] != d or s < n or time >= ti + timedelta(hours=6):
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
        while d != date2 and ti <= ti2:
            star.append('\t'.join([d, str(dayStar)]))
            dayStar = 0
            d = datetime.strftime(ti + timedelta(days=1), '%Y%m%d')
            ti = datetime.strptime(d, '%Y%m%d')
        filename = 'data/momo/star-day/' + id + '.txt'
        print('save file:', filename)
        with open(filename, 'w') as f:
            f.write('\n'.join(star))


if __name__ == '__main__':
    main()
