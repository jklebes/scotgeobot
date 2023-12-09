from mastodon import Mastodon
from plyer import notification
import datetime

from checkStations import *
from checkCities import *
from calcGeohashes import *

#mastodon = Mastodon(access_token = 'token.secret', api_base_url = 'https://botsin.space/')

def newDates(dates, last_dates):
    if not last_dates:
        return True
    latest = max(dates)
    latest_previous = max(last_dates)
    return latest > latest_previous

datefile = "lastdates.txt"
dateformat = '%d-%m-%Y'

scotland_graticules= [ (60, -2), (60, -1), (60, 0), #Foula, Lerwick, Unst
        (59, -3), (59, -2), (59, -2), #Dounby, Balfour, Sumburgh
        (58, -7), (58, -6),(58, -5), (58,-4), (58, -3), (58, -2), # Mangersta, Stornoway, Lochinver, Tongue, Thurso, Kirkwall
        (57, -7), (57,-6), (57, -5), (57, -4), (57,-3), (57, -2), (57, -1), #South Uist, Skye, Ullapool, Inverness, Elgin, Aberdeen, Petrehead
        (56,-7), (56, -6), (56, -5), (56, -4), (56, -3), (56, -2), #Barra, Tobermory, Oban, Helensburgh, Perth, Dundee
        (55, -6), (55, -5), (55, -4), (55,-3), (55,-2), #Coleraine, Campbeltown, Glasgow, Edinburgh, Jedburgh
        (54,-5), (54, -4), (54, -3)] #Belfast, Douglas, Barrow-In-Furness

results = geohashes(scotland_graticules)
try:
    last_dates = []
    f = open(datefile,'r')
    line = f.readline().strip()
    while line:
        date = datetime.datetime.strptime(line, dateformat).date()
        last_dates.append(date)
        line = f.readline().strip()
    f.close()
except:
    last_dates = []
if newDates([date for (date,offset) in results], last_dates): #empty if no new stock opening data since last run
    hits=0
    for (date,offset) in results:
        # scotland-specific sign, subtract from negative longitudes
        coords = [(a+offset[0], b-offset[1]) for (a,b) in scotland_graticules]
        cities = checkCities(coords)
        for c in cities:
            text = "Geohash in " + c + " on " + str(date)
            #mastodon.status_post(text)
            notification.notify(title="Geohash",
                                message= text,
                                app_icon = "eksplore_icon_259210.ico",
                                timeout = 1)
            hits+=1
        stations = checkStations(coords)
        for (s,c) in stations:
            text = "Geohash near " + s + " station ("+ str(round(c[0],3)) +","+ str(round(c[1],3))+") on " + str(date) 
            #mastodon.status_post(text)
            notification.notify(title="Geohash",
                                message= text,
                                app_icon = "eksplore_icon_259210.ico",
                                timeout = 1)
            hits+=1
    if hits==0:
        notification.notify(title="Geohash", message="No hits", 
                                app_icon = "eksplore_icon_259210.ico",
                    timeout=1)
    #write dates to file
    f= open(datefile,'w')
    for (date, offset) in results:
        f.write(date.strftime(dateformat)+'\n')
    f.close()
else:
    notification.notify(title="Geohash", message="No new geohashes.", 
                                app_icon = "eksplore_icon_259210.ico",
                    timeout=1)
