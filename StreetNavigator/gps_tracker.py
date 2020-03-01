from math import sin, cos, sqrt, atan2, radians
import requests


def path_finder(origin, destination, travel_mode, debug=False):
    end_point = 'https://maps.googleapis.com/maps/api/directions/json?'
    api_key = 'Insert API KEY'
    nav_request = f'origin={origin}&destination={destination}&mode={travel_mode}&key={api_key}'
    req = end_point + nav_request
    resp = requests.get(req).json()
    routes = resp['routes']
    if debug:
        print(resp)

    return routes[0]['legs']


def get_distance(**coordinates):
    R = 6373.0
    lat1 = radians(coordinates['current_lat'])
    lon1 = radians(coordinates['current_lng'])
    lat2 = radians(coordinates['wanted_lat'])
    lon2 = radians(coordinates['wanted_lng'])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c * 1000





