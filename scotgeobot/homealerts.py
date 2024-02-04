import argparse
from plyer import notification
from os import path

from .calcGeohashes import geohashes, geohash_digits
from .mygeodist import dist_km
from .scotgeobot import (newDates, scotland_graticules,
                        datefile, dateformat, getLastDates, notify,
                         project_directory)
def get_home():
    # TODO what if no home is set?  Print instructions on how to set.
    f = open(path.join(project_directory,"data","home.txt"), 'r')
    return list(map(float, f.readline().strip().split()))
home = get_home()
homedist = 15

if __name__ == "__main__":
    tooting = False; #this module is meant to be rnu privately on desktop

    # argparser
    parser = argparse.ArgumentParser()
    # skip desktop alerts in favor of command line
    parser.add_argument('--desktop', action=argparse.BooleanOptionalAction, default=True)
    # force re-check of old dates
    parser.add_argument('-f', '--redo', action='store_true')
    # a debugging run would be '--redo' only and a production run would be '--toot' only

    args = parser.parse_args()
    redo = args.redo;
    desktop = args.desktop;

    last_dates = getLastDates(datefile, dateformat)

    dates_digits = geohash_digits()
    # empty if no new stock opening data since last run
    nd = newDates([date for (date, offset) in dates_digits], last_dates)
    if redo:
        nd = [date for date,offset in dates_digits];
    results = geohashes(scotland_graticules, [(date, offset)
                         for (date, offset) in dates_digits if date in nd])
    for date in results:
        for coord in results[date]:
            dist = dist_km(home, coord)
            # print(dist, date)
            if dist <= homedist:
                text = "Geohash " + str(round(dist)) + \
                    "km from me on " + str(date) + "!"
                # mastodon.status_post(text)
                notify(text)
