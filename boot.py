def network_connect():
    import network
    import config
    from utime import sleep

    sta_if = network.WLAN(network.STA_IF)
    while not sta_if.isconnected():
        for network in config.network:
            if not sta_if.isconnected():
                print('connecting to network ', network['name'], ' ...')
                sta_if.active(True)
                sta_if.connect(network['name'], network['pw'])
                sleep(10)
    print('network config:', sta_if.ifconfig())


def network_disconnect():
    import network
    network.WLAN(network.STA_IF).disconnect()


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
