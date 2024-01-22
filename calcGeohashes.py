"""
Module to fetch all current/future geohashes given a list of 
graticules with calcGeohashes.geohashes(coords) .
This program is NOT general, not w30 compliant:
TODO make general
It's only for coordinates east of -30 and west of (including) 0, 
which is good enough for all of Scotland.
This program relies on https://carabiner.peeron.com to post updates dow jones
hashes for geohashing.
"""

import hashlib
import datetime
import struct
from numpy import sign
from urllib.request import urlopen
from urllib.error import HTTPError
from collections import defaultdict

def geohash_digits(td30=1):
    """
    Gets geohash after-decimal digits for each available current and future date
    optional input: td30 = 1, default 1 because Scotland is all east of -30.
                    Use with 0 and 1 for global code.
    returns:  list of tuples (date, digits)
    """
    digits = []
    dates = []
    date = datetime.date.today()
    while True: #looping over available dates
        try:
            djia = urlopen((date - datetime.timedelta(td30)).strftime(
                "http://carabiner.peeron.com/xkcd/map/data/%Y/%m/%d")).read().decode('utf-8')
        except HTTPError:
            # no geohashes this far into the future, end loop
            break
        dates.append(date)
        # code from
        # https://geohashing.site/geohashing/Implementations/Libraries/Python
        # TODO missing step going from djia to dj?
        sum_ = hashlib.md5(bytes('{0}-{1}'.format(date, dj), 'utf-8')).digest()
        n, w = [x / 2. ** 64 for x in struct.unpack_from(">QQ", sum_)]
        digits.append((n,w))
        # increment date
        date += datetime.timedelta(days=1)
    return zip(dates, digits)



def geohashes(coords):
    """
    in: list of graticules to get geohashes for
    returns: dict {date: geohashes}
    """
    results = defaultdict(lambda: [])
    # TODO check all east of -30, assert / warn
    for (date, digits) in geohash_digits():
        for coord in coords:
            #construct geohash coord for each graticule
            north = coord[0]
            west = coord[1])
            geohash = (sign(north)*(abs(north)+digits[0]), sign(west)*(abs(west)+digits[1]))
            results[date].append(geohash)
    return results
