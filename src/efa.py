try:
    import uio as io
except:
    import io

try:
    import urequests as requests
except:
    import requests

import cet_time
import config
import naya.json


class Departure:
    def __init__(self, json_data, conf):
        departure_time = json_data['departureTime']
        self.delay = int(json_data['delay'])
        self.number = json_data['number']
        self.stopName = json_data['stopName']
        self.direction = json_data['direction']
        self.departure_in_seconds_since_epoch = cet_time.mktime(
            int(departure_time['year']), int(departure_time['month']), int(departure_time['day']),
            int(departure_time['hour']),
            int(departure_time['minute']))
        self.departure_time_formatted = '{:02d}:{:02d}'.format(int(departure_time['hour']),
                                                               int(departure_time['minute']))
        self.walking_distance_in_minutes = conf['distance_in_minutes']
        self.name = conf['name']
    
    def time_to_leaf_in_seconds_since_epoch(self):
        return self.departure_in_seconds_since_epoch - self.walking_distance_in_minutes * 60

    def __repr__(self):
        return '{:5s} {:3s} {:02d} {:2s} {}'.format(self.departure_time_formatted, self.number, self.delay,
                                                    self.name,
                                                    self.time_to_leaf_in_seconds_since_epoch())
    
    def reachable(self, seconds_since_epoch):
        return self.time_to_leaf_in_seconds_since_epoch() >= int(seconds_since_epoch)
    
    def remaining_minutes(self, seconds_since_epoch):
        return int((self.time_to_leaf_in_seconds_since_epoch() - int(seconds_since_epoch)) / 60)
    
    def get_key(self):
        return self.departure_in_seconds_since_epoch


class _CharStream:
    def __init__(self, bytestream):
        self.bytestream = bytestream
        self.buffer = list()
    
    def close(self):
        self.bytestream.close()
    
    def read(self, size):
        if size == 1:
            return self.read_one()
        else:
            raise NotImplementedError()
    
    def read_one(self):
        answer = None
        b = self.bytestream.read(1)
        if b is None:
            pass
        else:
            try:
                self.buffer.append(b)
                answer = bytes([int.from_bytes(b, 'little') for b in self.buffer]).decode()
                self.buffer = list()
            except UnicodeError as u:
                answer = self.read_one()
        return answer


def departures():
    departure_list = []
    for station in config.efa_stations:
        departure_list = departure_list + _departures_for_station(station)
    return sorted(departure_list, key=Departure.get_key)


def _departures_for_station(station):
    print("")
    print("efa::station_name:", station['name'])
    print("efa::station:", station)
    url = config.efa_departure_rest_endpoint_template.format(station['id'])
    print("efa::url:", url)
    request = requests.get(url, stream=True)
    print("efa::status_code:", request.status_code)
    print("efa::wrapping bytes")
    station_json_stream = _CharStream(request.raw)
    answer = []
    try:
        limit = station['fetchLimit']
        items = naya.json.stream_array(naya.json.tokenize(station_json_stream))
        if limit > 0:
            for item in items:
                if item['number'] in station['numbers']:
                    if item['direction'] in station['directions']:
                        departure = Departure(item, station)
                        print("- ", limit, departure)
                        answer.append(departure)
                        limit = limit - 1
                        if limit <= 0:
                            return answer
    finally:
        request.close()
        station_json_stream.close()
    return answer
