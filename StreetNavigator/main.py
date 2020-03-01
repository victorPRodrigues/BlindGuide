import gps_tracker
from math import sin, cos, sqrt, atan2, radians

ORIGIN = 'Lanches Mac Fei, Av. Humberto A C Branco, 3972 - Assunção, São Bernardo do Campo - SP, 09850-305'.replace(' ',
                                                                                                                    '+')
DESTINATION = '-23.7259703,-46.5797997'
TRAVEL_MODE = 'walking'

path_data = gps_tracker.path_finder(ORIGIN, DESTINATION, TRAVEL_MODE)
path_steps = path_data[0]['steps']

# The first step (path_steps[0]) is an overview of the array

#for i in range(1, len(path_steps)):
#    dist = gps_tracker.get_distance(current_lat=)

print(gps_tracker.get_distance(current_lat=-23.725198, current_lng=-46.581013,
                               wanted_lat=path_steps[0]['end_location']['lat'],
                               wanted_lng=path_steps[0]['end_location']['lng']))


