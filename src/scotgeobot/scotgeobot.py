from scotgeobot.calcGeohashes import *
from scotgeobot.checkCities import *
from scotgeobot.checkStations import *
from plyer import notification
from os import path
import warnings
import datetime
import argparse

project_directory = path.dirname(path.abspath(__file__))

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
        try:
            notification.notify(title="Geohash",
                            message=message,
                            app_icon="eksplore_icon_259210.ico",
                            timeout=1)
        except:
            warnings.warn("Desktop notification failed")
            desktop = False
    if tooting:
        #TODO post rest as thread
        #TODO this is character limit for botsin.space, fetch from instance?
        if len(message) > 500:
            message = message[:501]
        try:
            mastodon_account.status_post(message)
        except:
            warnings.warn("Toot failed to post")
            tooting = False
    if not desktop and not tooting:
        print(" ########### Geohash ########### ")
        print(message)
        print(" ############################### \n\n")


datefile = path.join(project_directory,"data", "lastdates.txt")
dateformat = '%d-%m-%Y'

# Scotland graticule integer parts, with name according to geohashing wiki noted
# Some are included despite having no major cities or mainland-connected railway stations - this could be left out.
# Some are included despite mostly being in Ireland, England - its necessary if they contain scottish towns ans stations
# and not a problem because railway stations will be filtered for being on Scotland/England main landmass.
# Some southern graticules contain only England, they are included as potentially interesting and reachable
# to a geohasher in southern scotland going for a minesweeper.
scotland_graticules = [(60, -2), (60, -1), (60, 0),  # Foula, Lerwick, Unst

                       (59, -3), (59, -2), (59, -2), # Dounby, Balfour, Sumburgh

                       (58, -7), (58, -6), (58, -5), (58, -4), (58, -3), (58, -2),
                       # Mangersta, Stornoway, Lochinver, Tongue, Thurso, Kirkwall

                       (57, -7), (57, -6), (57, -5), (57, - \
                                                      4), (57, -3), (57, -2), (57, -1),
                       # South Uist, Skye, Ullapool, Inverness, Elgin,
                       # Aberdeen, Peterhead

                       (56, -7), (56, -6), (56, -5), (56, -4), (56, -3), (56, -2),
                       # Barra, Tobermory, Oban, Helensburgh, Perth, Dundee

                       (55, -6), (55, -5), (55, -4), (55, -3), (55, -2),
                       # Coleraine, Campbeltown, Glasgow, Edinburgh, Jedburgh

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
