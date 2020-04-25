import gps_tracker
import detector
import RPi.GPIO as GPIO
import time

gps_tracker.play_sound_notification('welcome')

while True:
    try:
        current_location = gps_tracker.get_current_location()
        if current_location != (0.0, 0.0):
            break
        
    except:
        continue

# Google MAPS Direction API Request
org = 'Lanches Mac Fei, Av. Humberto A C Branco, 3972 - Assunção, São Bernardo do Campo - SP, 09850-305'.replace(' ',
                                                                                                                 '+')
destination = '-23.7259703,-46.5797997'
travel_mode = 'walking'
resp = gps_tracker.path_finder(org, destination, travel_mode)
steps = resp[0]['steps']

street_crosser = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(street_crosser, GPIO.IN)

# Path Tracking & Navigation
for index, step in enumerate(steps):
    if not(index):
        gps_tracker.play_sound_notification("ready")

    elif len(step['maneuver'].strip()):
        gps_tracker.play_sound_notification(step['maneuver'])

    distance = step['distance']['value']
    while distance >= 1:
        if GPIO.input(street_crosser):
            time.sleep(0.5)
            detector.street_crosser()

        current_location = gps_tracker.get_current_location()
        distance = gps_tracker.get_distance(current_lat=current_location[0], 
                                            current_lng=current_location[1],
                                            wanted_lat=step['end_location']['lat'],
                                            wanted_lng=step['end_location']['lng'])
        
        if distance <= 2.5:
            gps_tracker.play_sound_notification("2m" + steps[index + 1]['maneuver'])
        
        elif distance <= 1.7:
            gps_tracker.play_sound_notification("1m" + steps[index + 1]['maneuver'])

        print(distance)

gps_tracker.play_sound_notification("reached")
time.sleep(2)
gps_tracker.play_sound_notification("ending_presentation")
GPIO.cleanup()