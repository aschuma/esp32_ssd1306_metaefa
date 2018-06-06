import machine
import micropython
import time

import cet_time
import display
import efa
import timer

micropython.alloc_emergency_exception_buf(100)


class View:
    def __init__(self):
        self.error = None
        self.departures = []
        self.processing = False
        self.message = None
    
    @staticmethod
    def format_departure(departure):
        now = time.time()
        remaining_minutes = departure.remaining_minutes(now)
        departure_delay_formatted = '{:>3s}'.format('+' + str(departure.delay)) if departure.delay > 0 else '   '
        return '{:2s} {:2d}min {} {}'.format(departure.number, remaining_minutes, departure_delay_formatted, departure.name)
    
    def show_error(self, error):
        self.error = str(error)
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
        oled.text(cet_time.current_time_formatted(), 0, 0)
        if self.error:
            oled.text('ERROR', 0, 26)
            oled.text(self.error, 0, 38)
        elif self.message:
            oled.fill(0)
            oled.text(str(self.message), 0, 0)
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
            reachable = self.reachable_departures()
            if len(self.departures) > 0:
                oled.text(self.format_departure(reachable[0]), 0, 14)
            if len(self.departures) > 1:
                oled.text(self.format_departure(reachable[1]), 0, 26)
            if len(self.departures) > 2:
                oled.text(self.format_departure(reachable[2]), 0, 38)
            if len(self.departures) > 3:
                oled.text(self.format_departure(reachable[3]), 0, 50)
        if self.processing:
            oled.fill_rect(0, 62, 128, 20, 1)
        oled.show()
    
    def reachable_departures(self):
        now = time.time()
        return [departure for departure in self.departures if departure.reachable(now)]


view = View()

i2c = machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5))
oled = display.Display(i2c)

scheduler = timer.default(lambda: view.paint(oled)).start()


def stop():
    print("Shuting down")
    scheduler.stop()


counter = 0

try:
    view.show_message('Booting...')
    time.sleep(2)
    network_connect(lambda: view.show_message('Network...'))
    ntp_time_sync(lambda: view.show_message('NTP...'))
    view.show_message('EFA...')
except Exception as e:
    view.show_error(e)
    view.paint(oled)
else:
    while True:
        counter = counter + 1
        try:
            view.show_progress(True)
            network_connect(lambda: view.show_message('Network...'))
            departures = efa.departures()
            view.show_departures(departures)
        except Exception as e:
            print(e)
            view.show_error(e)
        finally:
            view.show_progress(False)
        time.sleep(75)
        if counter % 100 == 0:
            ntp_time_sync(lambda: view.show_message('NTP...'))
finally:
    stop()

