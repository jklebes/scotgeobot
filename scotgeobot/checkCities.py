import shapely
from .mygeodist import dist_km


def checkCities(coords):
    results = []
    names_poly = ['Edinburgh', 'Glasgow', 'Dundee',
                  'Aberdeen']  # cities with .poly files
    for name in names_poly:
        filename = name + '.geojson'
        f = open(filename, 'r')
        filetext = f.read()
        f.close()
        p = shapely.from_geojson(filetext)
        for coord in coords:
            coord_ = shapely.Point((coord[1], coord[0]))
            # print(name, coord, p.contains(coord_))
            if p.contains(coord_):
                results.append(name)
    # read names_circles, centers, radii from file
    f = open('cities.txt', 'r')
    names_circles = dict([])
    line = f.readline()
    while line:
        (name, lat, lon, rad) = line.strip().split()
        if name not in names_poly:
            names_circles[name] = ((float(lat), float(lon)), float(rad))
        line = f.readline()
    f.close()
    for name in names_circles:
        for coord in coords:
            (center, radius) = names_circles[name]
            if dist_km(coord, center) <= radius:
                results.append(name)
    return results
