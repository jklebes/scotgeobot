from scotgeobot.calcGeohashes import *
from scotgeobot.checkCities import *
from scotgeobot.checkStations import *
from plyer import notification
from os import path
import datetime
import argparse

project_directory = path.dirname(path.dirname(path.abspath(__file__)))

def newDates(dates, last_dates):
    if not last_dates:
        return dates
    if not dates:
        return []
    latest = max(dates)
    latest_previous = max(last_dates)
    if latest <= latest_previous:
        return []
    results = []
    for d in dates:
        if d not in last_dates:
            results.append(d)
    return results

def notify(message, desktop=False, tooting=False, mastodon_account=None):
    """depending on setting, ouput the message to terminal or
    desktop notifications; toot bot broadcast or not"""
    if desktop:
        notification.notify(title="Geohash",
                            message=message,
                            app_icon="eksplore_icon_259210.ico",
                            timeout=1)
    else:
        print(" ########### Geohash ########### ")
        print(message)
        print(" ############################### \n\n")
    if tooting:
        mastodon_account.status_post(message);


datefile = path.join(project_directory,"data", "lastdates.txt")
dateformat = '%d-%m-%Y'

# Scotland graticule integer parts, with name according to geohashing wiki noted
# Some are included despite having no major cities or mainland-connected railway stations - this could be left out.
# Some are included despite mostly being in Ireland, England - its necessary if they contain scottish towns ans stations
# and not a problem because railway stations will be filtered for being on Scotland/England main landmass.
# Some southern graticules contain only England, they are included as potentially interesting and reachable
# to a geohasher in southern scotland going for a minesweeper.
scotland_graticules = [(60, -2), (60, -1), (60, 0),  # Foula, Lerwick, Unst
                       # Dounby, Balfour, Sumburgh
                       (59, -3), (59, -2), (59, -2),
                       # Mangersta, Stornoway, Lochinver, Tongue, Thurso, Kirkwall
                       (58, -7), (58, -6), (58, -5), (58, -4), (58, -3), (58, -2),
                       # South Uist, Skye, Ullapool, Inverness, Elgin,
                       # Aberdeen, Peterhead
                       (57, -7), (57, -6), (57, -5), (57, - \
                                                      4), (57, -3), (57, -2), (57, -1),
                       # Barra, Tobermory, Oban, Helensburgh, Perth, Dundee
                       (56, -7), (56, -6), (56, -5), (56, -4), (56, -3), (56, -2),
                       # Coleraine, Campbeltown, Glasgow, Edinburgh, Jedburgh
                       (55, -6), (55, -5), (55, -4), (55, -3), (55, -2),
                       (54, -5), (54, -4), (54, -3)]  # Belfast, Douglas, Barrow-In-Furness

def getLastDates(datefile, dateformat):
    try:
        last_dates = []
        f = open(datefile, 'r')
        line = f.readline().strip()
        while line:
            date = datetime.datetime.strptime(line, dateformat).date()
            last_dates.append(date)
            line = f.readline().strip()
        f.close()
    except BaseException:
        last_dates = []
    return last_dates

if __name__=="__main__":
    # argparser
    parser = argparse.ArgumentParser()
    # whether to broadcast
    parser.add_argument('--toot', action='store_true')
    # skip desktop alerts in favor of command line
    parser.add_argument('--desktop', action=argparse.BooleanOptionalAction, default=True)
    # force re-check of old dates
    parser.add_argument('-f', '--redo', action='store_true')

    # a debugging run would be '--redo -no--desktop' and a production run would be '--toot' only
    args = parser.parse_args()
    tooting = args.toot;
    desktop = args.desktop;
    redo = args.redo;
    if tooting:
        from mastodon import Mastodon
        assert(path.isfile(path.join(project_dir,"data","token.secret")))
        mastodon_account = Mastodon(
            access_token=path.join(project_dir,"data","token.secret"),
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

    # write dates to file
    f = open(datefile, 'w')
    for (date, offset) in dates_digits:
        f.write(date.strftime(dateformat) + '\n')
    f.close()
