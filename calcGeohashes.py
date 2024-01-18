import hashlib
import datetime
import struct
from urllib.request import urlopen
from urllib.error import HTTPError


def djs():
    djs = []
    dates = []
    date = datetime.date.today()
    td30 = 1  # scotland is east of -30
    # start yesterday for testing
    # date -= datetime.timedelta(days=1)
    while True:
        try:
            djia = urlopen((date - datetime.timedelta(td30)).strftime(
                "http://carabiner.peeron.com/xkcd/map/data/%Y/%m/%d")).read().decode('utf-8')
        except HTTPError:
            break
        dates.append(date)
        djs.append(djia)
        date += datetime.timedelta(days=1)
    return zip(dates, djs)


def geohash(coord, date, dj):
    # code from
    # https://geohashing.site/geohashing/Implementations/Libraries/Python
    myLat = int(coord[0])
    myLon = int(coord[1])
    if myLat < 0:
        south = -1
    else:
        south = 1
    if myLon < 0:
        west = -1
    else:
        west = 1
    sum_ = hashlib.md5(bytes('{0}-{1}'.format(date, dj), 'utf-8')).digest()
    n, w = [d * (abs(a) + f) for d, f, a in zip((south, west), [x / 2. **
                                                                64 for x in struct.unpack_from(">QQ", sum_)], [myLat, myLon])]
    return (n, w)


def geohashes():
    results = []
    dj_results = djs()
    for (date, dj) in dj_results:
        results.append((date, geohash((0, 0), date, dj)))
    return results
