from math import sin, cos, sqrt, atan2, radians
import requests
import serial
import pynmea2


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


def get_current_location():
    port = serial.Serial('/dev/serial0', 9600, timeout=0.5)
    while True:
        while port.inWaiting() == 0:
            pass
        msg = port.readline()
        line = str(msg)
        if (line[2:8] == "$GPGLL"):
            parsed_msg = pynmea2.parse(msg.decode('utf-8'))
            lat = parsed_msg.latitude
            long = parsed_msg.longitude
            return ((lat, long))


def get_distance(**coordinates):
    R = 6373.0
    lat1 = radians(coordinates['current_lat'])
    lon1 = radians(coordinates['current_lng'])
    lat2 = radians(coordinates['wanted_lat'])
    lon2 = radians(coordinates['wanted_lng'])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c * 1000


def play_sound_notification(maneuver):
    FILES_PATH = "/home/pi/DesktopBlindGuide/Audio_Nav_Files"
