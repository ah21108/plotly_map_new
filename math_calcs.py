# https://www.movable-type.co.uk/scripts/latlong.html

'''
Distance
This uses the ‘haversine’ formula to calculate the great-circle 
distance between two points – that is, the shortest distance over 
the earth’s surface – giving an ‘as-the-crow-flies’ distance 
between the points (ignoring any hills they fly over, of course!).

Haversine
formula:	a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
c = 2 ⋅ atan2( √a, √(1−a) )
d = R ⋅ c
where	φ is latitude, λ is longitude, R is earth’s radius (mean radius = 6,371km);
note that angles need to be in radians to pass to trig functions!
JavaScript:	
const R = 6371e3; // metres
const φ1 = lat1 * Math.PI/180; // φ, λ in radians
const φ2 = lat2 * Math.PI/180;
const Δφ = (lat2-lat1) * Math.PI/180;
const Δλ = (lon2-lon1) * Math.PI/180;

const a = Math.sin(Δφ/2) * Math.sin(Δφ/2) +
          Math.cos(φ1) * Math.cos(φ2) *
          Math.sin(Δλ/2) * Math.sin(Δλ/2);
const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));

const d = R * c; // in metres
'''
from math import radians, cos, sin, asin, sqrt
def haversine(lon1, lat1, lon2, lat2):
    '''
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees).
    Taken from https://stackoverflow.com/questions/4913349/haversine
    -formula-in-python-bearing-and-distance-between-two-gps-points
    Verified against https://www.omnicalculator.com/math/great-circle 
    to within 0.1 km across random values pos and neg lat/long.

    inputs:
    ----------
    lon1: float, range[-180, 180].  Longitude of point 1
    lat1: float, range[-90, 90].    Latitude of point 1
    lon2: float, range[-180, 180].  Longitude of point 2
    lat2: float, range[-90, 90].    Latitude of point 2

    outputs:
    ----------
    distance between point 1 and point 2 in km.

    '''
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r


r = 6371000  #earth's radius; meters
lat1, long1 = (45,-70)
lat2, long2 = (-45,45)

dist = haversine(long1, lat1, long2, lat2)
print(dist)
