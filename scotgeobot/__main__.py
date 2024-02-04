from scotgeobot.calcGeohashes import *
from scotgeobot.checkCities import *
from scotgeobot.checkStations import *
from scotgeobot.scotgeobot import *
from scotgeobot.homealerts import *
from plyer import notification
from os import path
import datetime
import argparse


if __name__=="__main__":
    # TODO make arg parsing a function in scotgeobot?
    # argparser
    parser = argparse.ArgumentParser()
    # whether to broadcast
    parser.add_argument('--toot', action='store_true')
    # skip desktop alerts in favor of command line
    parser.add_argument('--desktop', action=argparse.BooleanOptionalAction, default=True)
    # force re-check of old dates
    parser.add_argument('-f', '--redo', action='store_true')
    # include homealert in main module run?
    parser.add_argument('--homealert', action='store_true')

    # a debugging run would be '--redo -no--desktop' and a production run would be '--toot' only
    args = parser.parse_args()
    tooting = args.toot;
    desktop = args.desktop;
    redo = args.redo;
    homealert = args.homealert;

    if tooting:
        from mastodon import Mastodon
        mastodon = Mastodon(
            access_token='token.secret',
            api_base_url='https://botsin.space/')


    last_dates= getLastDates(datefile=datefile, dateformat=dateformat)
    dates_digits = geohash_digits()
    nd = newDates([date for (date, offset) in dates_digits], last_dates)
    if redo:
        nd = [date for date,offset in dates_digits];
    results = geohashes(scotland_graticules, [(date, offset)
                     for (date, offset) in dates_digits if date in nd])
    hits=0
    for date in results:
        coords=results[date]
        # scotland-specific sign, subtract from negative longitudes
        cities = checkCities(coords)
        for c in cities:
            text = "Geohash in " + c + " on " + date.strftime(dateformat) + "."
            notify(text,desktop, tooting)
            hits += 1
        stations = checkStations(coords)  # dict listos of (s,c) by graticule
        for g in stations:
            stations_graticule = stations[g]
            text = "Geohash near "
            for s, c in stations_graticule[:-1]:
                if s.split()[-1] == "Station":
                    text = text + s + \
                        " (" + str(round(c[0], 3)) + ", " + str(round(c[1], 3)) + "), "
                else:
                    text = text + s + \
                        " station (" + str(round(c[0], 3)) + ", " + str(round(c[1], 3)) + "), "
            (s, c) = stations_graticule[-1]
            if len(stations_graticule) > 1:
                text = text + "and "
            if s.split()[-1] == "Station":
                text = text + s + \
                    " (" + str(round(c[0], 3)) + ", " + str(round(c[1], 3)) + ") "
            else:
                text = text + s + \
                    " station (" + str(round(c[0], 3)) + ", " + str(round(c[1], 3)) + ") "
            text = text + "on " + date.strftime(dateformat) + "."
            notify(text, desktop, tooting)
            hits += 1
        if homealert:
            for coord in results[date]:
                dist = dist_km(home, coord)
                # print(dist, date)
                if dist <= homedist:
                    text = "Geohash " + str(round(dist)) + \
                        "km from me on " + str(date) + "!"
                    # mastodon.status_post(text)
                    notify(text, desktop, tooting)

    # write dates to file
    f = open(datefile, 'w')
    for (date, offset) in dates_digits:
        f.write(date.strftime(dateformat) + '\n')
    f.close()
