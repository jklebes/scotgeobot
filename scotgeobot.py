from calcGeohashes import *
from checkCities import *
from checkStations import *
import datetime
from plyer import notification
tooting = True
if tooting:
    from mastodon import Mastodon


if tooting:
    mastodon = Mastodon(
        access_token='token.secret',
        api_base_url='https://botsin.space/')


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


datefile = "lastdates.txt"
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

results = geohashes()


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


last_dates = getLastDates(datefile, dateformat)
# empty if no new stock opening data since last run
nd = newDates([date for (date, offset) in results], last_dates)
hits = 0
for date, offset in [(date, offset)
                     for (date, offset) in results if date in nd]:
    # scotland-specific sign, subtract from negative longitudes
    coords = [(a + offset[0], b - offset[1]) for (a, b) in scotland_graticules]
    cities = checkCities(coords)
    for c in cities:
        text = "Geohash in " + c + " on " + date.strftime(dateformat) + "."
        if tooting:
            mastodon.status_post(text)
        notification.notify(title="Geohash",
                            message=text,
                            app_icon="eksplore_icon_259210.ico",
                            timeout=1)
        hits += 1
    stations = checkStations(coords)  # dict listos of (s,c) by graticule
    for g in stations:
        stations_graticule = stations[g]
        text = "Geohash near "
        print(stations[g])
        print(stations_graticule[:-1])
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
        if tooting:
            mastodon.status_post(text)
        notification.notify(title="Geohash",
                            message=text,
                            app_icon="eksplore_icon_259210.ico",
                            timeout=1)
        hits += 1
# if hits==0:
    # notification.notify(title="Geohash", message="No hits",
    #                            app_icon = "eksplore_icon_259210.ico",
    #                timeout=1)
# write dates to file
f = open(datefile, 'w')
for (date, offset) in results:
    f.write(date.strftime(dateformat) + '\n')
f.close()
