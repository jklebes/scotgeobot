from collections import defaultdict
from .mygeodist import dist_km

radius = 4  # check 5km around stations?


def checkStations(coords):
    # list of stations as tuples (name, coord) per graticule
    results = defaultdict(lambda: [])
    f = open('stations.txt', 'r')
    stations = dict([])
    line = f.readline()
    while line:
        (name, lat, lon) = line.split(',')
        stations[name] = ((float(lat), float(lon)))
        line = f.readline()
    f.close()
    for name in stations:
        for coord in coords:
            center = stations[name]
            if dist_km(coord, center) <= radius:
                results[coord].append((name, center))
    return results
