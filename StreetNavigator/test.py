import gps_tracker
import detector
import RPi.GPIO as GPIO
import time
GPIO.cleanup()
gps_tracker.play_sound_notification('welcome')

while True:
    try:
        current_location = gps_tracker.get_current_location()
        if current_location != (0.0, 0.0):
            break

    except:
        continue

gps_tracker.play_sound_notification("ready")

street_crosser = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(street_crosser, GPIO.IN)

while True:
    if not(GPIO.input(street_crosser)):
        time.sleep(0.5)
        detector.street_crosser()
        GPIO.cleanup()
        break