try:
    import uio as io
except:
    import io

try:
    import urequests as requests
except:
    import requests

import config
import naya.json


class Departure:
    def __init__(self, json_data, conf):
        departure_time = json_data['departureTime']
        self.delay = json_data['delay']
        self.number = json_data['number']
        self.stopName = json_data['stopName']
        self.direction = json_data['direction']
        self.departure = (
            int(departure_time['year']), int(departure_time['month']), int(departure_time['day']),
            int(departure_time['hour']),
            int(departure_time['minute']), 0)
        self.distance_in_minutes = conf['distance_in_minutes']
        self.name = conf['name']

    def __repr__(self):
        return '{} {} {} {} {}'.format(self.departure, self.delay, self.name, self.direction, self.number)

    def get_key(self):
        return self.departure


def departures():

    departure_list = []
    for station in config.efa_stations: 
        departure_list = departure_list + departures_for_station(station)
    return sorted(departure_list,key=Departure.get_key)


def departures_for_station(station):
    print("STATION:", station)
    # get the raw data
    url = config.efa_departure_rest_endpoint_template.format(station['id'])
    print(" URL:", url)
    request = requests.get(url, stream=True)
    data = io.StringIO(request.text)
    request.close()    
    # extract data from json
    limit = station['fetchLimit']
    items = naya.json.stream_array(naya.json.tokenize(data))
    answer = []
    if limit > 0:
        for item in items:        
            if item['number'] in station['numbers']:
                if item['direction'] in station['directions']:
                    departure = Departure(item, station)
                    print(" - ", limit, departure)
                    answer.append(departure)
                    limit = limit - 1
                    if limit <= 0:
                        return answer                        
    return answer
