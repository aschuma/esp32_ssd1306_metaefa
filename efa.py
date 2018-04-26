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
        print(json_data)
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


def departures():
    departure_list = []
    for station in config.efa_stations:
        print(station)
        limit = station['fetchLimit']
        request = requests.get(config.efa_departure_rest_endpoint_template.format(station['id']), stream=True)
        data = io.StringIO(request.text)
        request.close()
        items = naya.json.stream_array(naya.json.tokenize(data))
        departure_list = departure_list + ([
                                               Departure(item, station)
                                               for item in items
                                               if (
                        item['number'] in station['numbers'] and item['direction'] in station['directions'])][:limit])
    return departure_list
