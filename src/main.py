import machine
import time

import cet_time
import display
import efa


def reachable_departures(departure_list):
    now = cet_time.current()
    return [departure for departure in departure_list if departure.reachable(now)]


def format_departure(departure):
    now = cet_time.current()
    return '{:2s} {:2d}min {:02d} {}'.format(departure.number, departure.remaining_minutes(now), departure.delay,
                                                departure.name)
                        

i2c = machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5))
oled = display.Display(i2c)

oled.fill(0)
oled.center_fill_circle(0.6, 0)
oled.center_fill_circle(0.5, 1)
oled.center_fill_circle(0.4, 0)
oled.center_fill_circle(0.3, 1)
oled.center_fill_circle(0.2, 0)
oled.center_fill_circle(0.1, 1)
oled.show()

network_connect()

oled.invert(1)
oled.show()

ntp_time_sync()

oled.invert(0)
oled.show()

t = cet_time.current()
tstr = '{:04d}-{:02d}-{:02d} {:02d}:{:02d}'.format(t[0], t[1], t[2], t[3], t[4])

oled.fill(0)
oled.text(tstr, 1, int(oled.height / 2.0) - 8)
oled.invert(0)
oled.show()

while True:
    oled.fill_rect(0, 62, 128, 20, 1)
    oled.show()
    #
    try:
        departures = reachable_departures(efa.departures())
        #
        line0 = format_departure(departures[0])
        line1 = format_departure(departures[1])
        line2 = format_departure(departures[2])
        line3 = format_departure(departures[3])
        oled.fill(0)
        oled.invert(0)
        oled.text(cet_time.current_time_formatted(), 3, 3)
        oled.text(line0, 3, 18)
        oled.text(line1, 3, 28)
        oled.text(line2, 3, 38)
        oled.text(line3, 3, 48)
        oled.show()
    except Exception as e:
        print(e)
        oled.fill(0)
        oled.text(cet_time.current_time_formatted(), 3, 3)
        oled.text('Error', 3, 28)
        oled.text(str(e), 3, 38)
        oled.invert(1)
        oled.show()
    #
    #
    time.sleep(45)
