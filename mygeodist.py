"""
A function dist_km that calculates the geodesic distance in km between two 
points in (lat, long) format.  Approximate, for short local distances only.
"""

import math

# conversion factor coords to km based on your latitude
def deg_lat_to_km(dist, lat=56):
    """converts North-South distance from degrees to km,
    in this approzimation latitude arguement is irrelevant."""
    # constant conversion factor assuming earth is a sphere
    # a degree latitude is about 111.2km
    return dist * 111.2


def deg_lon_to_km(dist, lat):
    """converts East-West distance from degrees to km at a certain latitude."""
    # 111.195 = pi/180*earthradius
    return dist * (111.195 * math.cos(math.radians(lat)))


def dist_km(point1, point2):
    """geodesic distance between two points on earth.
    A point is a tuple (lon, lat) in degrees.
    This works for short local distances only, 
    latitude-dependednt deg to distance conversion factor 
    is assumed to be constant and taken from point1."""
    lat = point1[0]
    diff_lon = deg_lon_to_km(abs(point1[0] - point2[0]), lat)
    diff_lat = deg_lat_to_km(abs(point1[1] - point2[1]), lat)
    return math.sqrt(diff_lon**2 + diff_lat**2)
