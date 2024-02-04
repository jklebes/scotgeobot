"""
Module to fetch all current/future geohashes given a list of
graticules with calcGeohashes.geohashes(coords) .
This program is NOT general, not w30 compliant:
It's only for coordinates east of -30,
which is good enough for all of Scotland.
This program relies on https://carabiner.peeron.com to post updated dow jones
hashes for geohashing daily.
"""

import hashlib
import datetime
import struct
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
    while True:  # looping over available dates
        try:
            # TODO "consider using with;"
            dj = urlopen((date - datetime.timedelta(td30)).strftime(
                "http://carabiner.peeron.com/xkcd/map/data/%Y/%m/%d")).read().decode('utf-8')
        except HTTPError:
            # no geohashes this far into the future, end loop
            break
        dates.append(date)
        # code from
        # https://geohashing.site/geohashing/Implementations/Libraries/Python
        sum_ = hashlib.md5(bytes('{0}-{1}'.format(date, dj), 'utf-8')).digest()
        north_digits, west_digits = [x / 2. ** 64 for x in struct.unpack_from(">QQ", sum_)]
        digits.append((north_digits, west_digits))
        # increment date
        date += datetime.timedelta(days=1)
    return list(zip(dates, digits))



def geohashes(coords, geohash_digits=None):
    """
    input: list of graticules to get geohashes for
    optional input: geohash_digits list such as one previously generated by geohash_digits().
        Format [(date, (north_digits, west_digits)), ...]
        We might run geohash_digits() once to check whether new dates are available and whether 
        to proceed, then resuse it to generate all geohashes.
    returns: dict {date: geohashes}
    """
    if geohash_digits is None:
        geohash_digits = geohash_digits()
    results = defaultdict(lambda: [])
    # TODO check all east of -30, assert / warn
    for (date, digits) in geohash_digits:
        for coord in coords:
            # construct geohash coord for each graticule
            north = coord[0]
            west = coord[1]
            # TODO think agai about 0
            sign_north = -1 if north < 0 else 1
            sign_west = -1 if west < 0 else 1
            geohash = (sign_north * (abs(north) +
                       digits[0]), sign_west * (abs(west) + digits[1]))
            results[date].append(geohash)
    return results