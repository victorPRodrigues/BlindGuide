import gps_tracker
import serial
import pynmea2 as nmea

# Google MAPS Direction API Request
org = 'Lanches Mac Fei, Av. Humberto A C Branco, 3972 - Assunção, São Bernardo do Campo - SP, 09850-305'.replace(' ',
                                                                                                                 '+')
destination = '-23.7259703,-46.5797997'
travel_mode = 'walking'
resp = gps_tracker.path_finder(org, destination, travel_mode)
steps = resp[0]['steps']

# Setting up GPS Module
port = '/dev/ttyAMA0'  # Tx Rx
serial = serial.Serial(port, boundrate=9600, timeout=0.5)
nmea.NMEAStreamReader()

# Path Tracking & Navigation
for step in steps:
    if len(step['maneuver'].strip()):
        print(step['maneuver'])

    distance = step['distance']['value']
    while distance > 1:
        gps_data = serial.readline()
        if gps_data[0:6] != "$GPRMC":
            gps_msg = nmea.parse(gps_data)
            cur_lat = gps_msg.latitude
            cur_lng = gps_msg.longitude
            distance = gps_tracker.get_distance(current_lat=cur_lat, current_lng=cur_lng,
                                                wanted_lat=step['end_location']['lat'],
                                                wanted_lng=step['end_location']['lng'])
