import gps_tracker


# Google MAPS Direction API Request
org = 'Lanches Mac Fei, Av. Humberto A C Branco, 3972 - Assunção, São Bernardo do Campo - SP, 09850-305'.replace(' ',
                                                                                                                 '+')
destination = '-23.7259703,-46.5797997'
travel_mode = 'walking'
resp = gps_tracker.path_finder(org, destination, travel_mode)
print(resp)
steps = resp[0]['steps']

# Path Tracking & Navigation
for step in steps:
    if len(step['maneuver'].strip()):
        print(step['maneuver'])

    distance = step['distance']['value']
    while distance >= 1:
        current_location = gps_tracker.get_current_location()
        distance = gps_tracker.get_distance(current_lat=current_location[0], 
                                            current_lng=current_location[1],
                                            wanted_lat=-23.683352,#step['end_location']['lat'],
                                            wanted_lng=-46.707435)#step['end_location']['lng'])
        print(distance)
