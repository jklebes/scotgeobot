from mygeodist import *

radius=4 #check 5km around stations?

def checkStations(coords):
    results = []
    f=open('stations.txt', 'r')
    stations = dict([])
    line = f.readline()
    while line:
        (name, lat, lon) = line.split(',');
        stations[name] = ((float(lat), float(lon)))
        line = f.readline()
    f.close()
    for name in stations:
        for coord in coords:
            center = stations[name]
            if dist_km(coord, center)<=radius:
                results.append((name, center))
    return results 
