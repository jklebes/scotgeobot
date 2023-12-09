import math

#conversion factor coords to km based on your latitude
def degLatToKm(dist, lat=56):
    #constant assuming earth is a sphere
    # a degree latitude is about 111.2km
    return dist*111.2

def degLonToKm(dist, lat):
    #111.195 = pi/180*earthradius
    return dist*(111.195*math.cos(math.radians(lat)))

def dist_km(p1, p2):
    lat = p1[0]
    assert(lat>50)
    diff_lon = degLonToKm(abs(p1[0]-p2[0]), lat)
    diff_lat = degLatToKm(abs(p1[1]-p2[1]), lat)
    return math.sqrt(diff_lon**2 + diff_lat**2)
