This bot notifies of geohashes in Scottish major cities and near railway stations in (or near) Scotland.  It can also alert of geohashes near the user's specified 'home' coordinate.  It posts desktop notifications or toots to mastodon.

### Install

Currently 

``pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple scotgeobot==0.0.10``

### Simple manual running

The main command to run the module is ``python -m scotgeobot``.  It takes (optional) flags:

``--desktop``, ``--no-desktop`` whether to post results as desktop notifications.  Default no desktop.

``--toot``, ``--no-toot`` whether to post notifications to mastodon (after configuring account and keys).  Default no tooting.

``--redo``, ``-f`` By default only newly available dates and hashes are checked, meaning there will be no output if run again on the same day.  For debug reasons this flag forces all to be run again.

If neither desktop nor toot notifications are turned on, output is to command line.  

A testing run might be 

``python -m scotgeobot --redo --null --homealert``

and a production run

``python -m scotgeobot --desktop --toot --homealert``.


Not yet available, flags TODO:

``--null``, ``-n`` Post a message even when no hits near stations, cities, or home are found.

``--homealert`` Check around the private location set in ``data/home.txt`` and post (desktop or command line only) alert.

### Cron job
New geohashes appear daily around 14:30 (Scotland).

To set up a cron job, open
``$ crontab -e``

and add a line such as

``40 */2 * * * /home/pi/scotgeobot/cronscript.sh``

- this one runs ``cronscript.sh`` on the 40th minute of every second hour.

It's ok to run more than once per day, there is no output unless new coordinates become available.

TODO have this generated and added on insall

### Home alerts
To recieve a personalized desktop alert of geohashes falling within 15km of their location, as specified in ``homealerts.py``,
the user should make a file home.txt containing their coordinates (space separated, a single line), for example 

55.19433 -3.02568

### Desktop notifications
TODO desktop notifications unlikely to work on Windows.

### Mastodon bot
Retrieve the Personal Access Token from a mastodon account (Development tab) and save it to a local file such as ``~/.mastodon/token.secret``. 

On first run with the --toot flag, you will be taken through interactive setup. 
Supply the server instance, such as ``botsin.space``, and the file location.

### Cities definition
Dundee, Edinburgh, Aberdeen, and Glasgow are defined by the boundaries of their corresponding council areas.  The polygon outlines are saved in geojson files.

Perth, Stirling, and Inverness cities do not have administrative boundaries corresponding to the city.  For example, Perth is in the large council area "Perth and Kinross".  These cities are instead defined by the circles listed in ``cities.txt``, centered on their administrative centers and with given radius in kilometers estimated to include the urban area.

Other smaller cities and towns will be captured by their railway stations.

All railway stations in mainland Scotland and in adjacent mainland England graticules, excluding themepark "toy" railways, are listed in ``stations.txt``.  Alers are given for geohashes falling within 5km of a station, as defined in ``checkStations.txt``.

