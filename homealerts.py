from plyer import notification

from calcGeohashes import geohashes
from mygeodist import dist_km
from scotgeobot import (newDates, scotland_graticules,
                        datefile, dateformat, getLastDates)


f = open("home.txt", 'r')
home = list(map(float, f.readline().strip().split()))
homedist = 15

last_dates = getLastDates(datefile, dateformat)

results = geohashes()
# empty if no new stock opening data since last run
nd = newDates([date for (date, offset) in results], last_dates)
for date, offset in [(date, offset)
                     for (date, offset) in results if date in nd]:
    coords = [(a + offset[0], b - offset[1]) for (a, b) in scotland_graticules]
    for coord in coords:
        dist = dist_km(home, coord)
        # print(dist, date)
        if dist <= homedist:
            text = "Geohash " + str(round(dist)) + \
                "km from me on " + str(date) + "!"
            # mastodon.status_post(text)
            notification.notify(title="Geohash",
                                message=text,
                                app_icon="eksplore_icon_259210.ico",
                                timeout=1)
