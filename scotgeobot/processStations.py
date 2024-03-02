# one-time process the detailed geojson file on all train stations in the
# north British Isles area down to a list of coordinates of those in
# mainland Scotland and England above latitude 54

import geojson
import shapely
from os import path

project_directory = path.dirname(path.abspath(__file__))
# read file
f = open(path.join(project_directory, "data", "stations_full.geojson"), 'r')
stations = geojson.load(f).features
f.close()

# read mainland polygon
f = open(path.join(project_directory, "data", "GBmainland.geojson"), 'r')
filecontents = f.read()
mainland = shapely.from_geojson(filecontents)
f.close()

# drop all info but name and coordinate
lines = []
for station in stations:
    # filter "tourism" stations on small railway loops
    tourism = False
    try:
        if station.usage == "tourism":
            tourism = True
    except AttributeError:
        try:
            if station.properties['usage'] == "tourism":
                tourism = True
        except (AttributeError, KeyError):
            # no "usage" field also ok
            pass
    # look for coord in "geometry", if it's a polygon use any point
    g = station.geometry
    if g.type == "Point":
        coord = g.coordinates
    elif g.type == "Polygon":
        coord = g.coordinates[0][0]
    elif g.type == "LineString":
        coord = g.coordinates[0]
    # parse into shapely Point object
    point = shapely.Point(coord)
    # filter by latitude
    if not tourism and coord[1] > 54.0 and mainland.contains(point):
        # look for name in "name", "properties.name", "reltags.name"
        try:
            name = station.name
        except AttributeError:
            try:
                name = station.properties['name']
            except (AttributeError, KeyError):
                try:
                    name = station.reltags['name']
                except (AttributeError, KeyError):
                    print("Could not find name in: ")
                    print(station)
        lines.append(name + ", " + str(coord[1]) + ", " + str(coord[0]))


# save names and coordinates to file
f = open(path.join(project_directory, "data", "stations.txt"), 'w')
f.write("\n".join(lines))
f.close()
