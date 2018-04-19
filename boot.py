def network_connect():
    import network
    import config

    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network ...')
        sta_if.active(True)
        sta_if.connect(config.network_name, config.network_pw)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())


def ntp_time_sync():
    import ntptime
    from utime import sleep, localtime

    print('fetching UTC time ...')
    time_set = False
    while not time_set:
        try:
            ntptime.settime()
            time_set = True
        except Exception as e:
            print('could not set time:', str(e))
            sleep(5)
        print('utc time:', str(localtime()))
