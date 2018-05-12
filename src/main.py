import machine
import time

import cet_time
import display
import efa
import timer


def reachable_departures(departure_list):
    now = time.time()
    return [departure for departure in departure_list if departure.reachable(now)]


class View:
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
    
    def show_error(self, error):
        self.error = error
        self.processing = False
        self.message = None
    
    def show_message(self, msg):
        self.error = None
        self.message = msg
    
    def show_departures(self, departures):
        self.error = None
        self.message = None
        self.departures = departures
    
    def show_progress(self, boolean):
        self.processing = boolean
    
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
            oled.corner_se_fill_circle(0.50, 1)
            oled.corner_se_fill_circle(0.45, 0)
            oled.corner_se_fill_circle(0.40, 1)
            oled.corner_se_fill_circle(0.35, 0)
            oled.corner_se_fill_circle(0.30, 1)
            oled.corner_se_fill_circle(0.25, 0)
            oled.corner_se_fill_circle(0.20, 1)
            oled.corner_se_fill_circle(0.15, 0)
            oled.corner_se_fill_circle(0.10, 1)
            oled.corner_se_fill_circle(0.05, 0)
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


view = View()

i2c = machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5))
oled = display.Display(i2c)

scheduler = timer.Scheduler(lambda: view.paint(oled))
scheduler.start()

try:
    view.show_message('Booting...')
    time.sleep(2)
    view.show_message('Network...')
    network_connect()
    view.show_message('NTP...')
    time.sleep(1)
    ntp_time_sync()
    view.show_message('EFA...')
except Exception as e:
    view.show_error(e)
    view.paint(oled)
    scheduler.stop()
else:
    while True:
        try:
            view.show_progress(True)
            departures = reachable_departures(efa.departures())
            view.show_departures(departures)
        except Exception as e:
            print(e)
            view.show_error(e)
        finally:
            view.show_progress(False)
        time.sleep(45)

