This bot notifies of geohashes in Scottish major cities and near railway stations in (or near) Scotland.  It can also alert of geohashes near the user's specified 'home' coordinate.  It posts desktop notifications or toots to mastodon.

### Cron job
New geohashes appear daily at around 14:30 (Scotland).  The program checks whether updated hashes have been posted (comparing to ``lastdates.txt``) and only gives desktop or social media notifications if the alerts are indeed new.  

To set up a cron job, open
``$ crontab -e``

and add a line such as

``40 */2 * * * /home/pi/scotgeobot/cronscript.sh``

- this one runs ``cronscript.sh`` on the 40th minute of every second hour.

TODO have this generated and added on insall

### Home alerts
To recieve a personalized desktop alert of geohashes falling within 15km of their location, as specified in ``homealerts.py``,
the user should make a file home.txt containing their coordinates (space separated, a single line), for example 

55.19433 -3.02568

### Mastodon bot

### Cities definition
Dundee, Edinburgh, Aberdeen, and Glasgow are defined by the boundaries of their corresponding council areas.  The polygon outlines are saved in geojson files.

Perth, Stirling, and Inverness cities do not have administrative boundaries corresponding to the city.  For example, Perth is in the large council area "Perth and Kinross".  These cities are instead defined by the circles listed in ``cities.txt``, centered on their administrative centers and with given radius in kilometers estimated to include the urban area.

Other smaller cities and towns will be captured by their railway stations.

All railway stations in mainland Scotland and in adjacent mainland England graticules, excluding themepark "toy" railways, are listed in ``stations.txt``.  Alers are given for geohashes falling within 5km of a station, as defined in ``checkStations.txt``.

