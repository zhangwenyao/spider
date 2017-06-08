import sys
from datetime import datetime, timedelta


def main(argv=sys.argv[1:]):
    infile = "infiles/momo-ids.txt"
    with open(infile, 'r') as f:
        ids = f.read().split()
    star = {}
    for id in ids:
        star = []
        filename = 'data/momo/star/' + id + '.txt'
        print('read file:', filename)
        with open(filename, 'r') as f:
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
                            print(data, t, n)
                            s = n
                    elif s.find('亿') >= 0:
                        s = s.replace('亿', '00000000')
                        s = int(s)
                        if n - 100000000 < s <= n - n % 100000000:
                            print(data, t, n)
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
                            print('long interval:', data, t, n)
                    n = s
                    t = data[0]
                    ti = time
        if t:
            star.append('\t'.join([t, str(n)]))
        filename = 'data/momo/star-time/' + id + '.txt'
        print('save file:', filename)
        with open(filename, 'w') as f:
            f.write('\n'.join(star))


if __name__ == '__main__':
    main()
