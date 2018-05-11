import machine
import time

import cet_time
import display
import efa
import timer


def reachable_departures(departure_list):
    now = time.time()
    return [departure for departure in departure_list if departure.reachable(now)]


class Model:
    def __init__(self):
        self.error = None
        self.departures = []
        self.processing = False
        self.message = None
    
    @staticmethod
    def format_departure(departure):
        now = time.time()
        return '{:2s} {:2d}min {:02d} {}'.format(departure.number, departure.remaining_minutes(now), departure.delay,
                                                 departure.name)
    
    def paint(self, oled):
        oled.fill(0)
        oled.invert(0)
        oled.text(cet_time.current_time_formatted(), 3, 3)
        if self.error:
            oled.text('Error', 3, 28)
            oled.text(str(self.error), 3, 38)
            oled.invert(1)
        elif self.message:
            oled.fill(0)
            oled.text(str(self.message), 3, 3)
            oled.center_fill_circle(0.3, 1)
            oled.center_fill_circle(0.2, 0)
            oled.center_fill_circle(0.1, 1)
        else:
            if len(self.departures) > 0:
                oled.text(self.format_departure(self.departures[0]), 3, 18)
            if len(self.departures) > 1:
                oled.text(self.format_departure(self.departures[1]), 3, 28)
            if len(self.departures) > 2:
                oled.text(self.format_departure(self.departures[2]), 3, 38)
            if len(self.departures) > 3:
                oled.text(self.format_departure(self.departures[3]), 3, 48)
        if self.processing:
            oled.fill_rect(0, 62, 128, 20, 1)
        oled.show()


model = Model()

i2c = machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5))
oled = display.Display(i2c)

scheduler = timer.Scheduler(lambda: model.paint(oled))
scheduler.start()

model.message = 'Network...'
model.processing = False

try:
    network_connect()
    model.message = 'NTP...'
    ntp_time_sync()
    model.message = 'EFA...'
except Exception as e:
    model.message = None
    model.error = str(e)
    model.message = False
    model.paint(oled)
    scheduler.stop()
else:
    while True:
        try:
            model.processing = True
            model.departures = reachable_departures(efa.departures())
            model.error = None
            model.message = None
        except Exception as e:
            print(e)
            model.error = e
        finally:
            model.processing = False
        time.sleep(45)
