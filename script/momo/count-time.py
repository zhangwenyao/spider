from datetime import datetime, timedelta


def main():
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
                d = int(data[1])
                if n <= 0:
                    n = d
                    t = data[0]
                    ti = time
                    if d <= 0:
                        continue
                if d > 0:
                    if d < n or time >= ti + timedelta(hours=6):
                        star.append('\t'.join([t, str(n)]))
                        if d >= n \
                           and ti + timedelta(hours=3) <= time \
                           <= ti + timedelta(hours=6):
                            print(t, data[0])
                    n = d
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
