def network_scan():
    import network
    
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    available_nw_names = [str(nw[0], 'UTF-8') for nw in sta_if.scan()]
    print('network::scan:', available_nw_names)
    return available_nw_names


def network_configurations():
    import config
    
    available_nw_names = network_scan()
    available_nw_config_list = [conf for conf in config.network for name in available_nw_names if conf['name'] == name]
    print('network::known:', [config['name'] for config in available_nw_config_list])
    return available_nw_config_list


def network_connect():
    import network
    from utime import sleep
    
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        config_list = network_configurations()
        config = config_list[0] if config_list else None
        if config:
            print('network::connecting:', config['name'])
            sta_if.active(True)
            sta_if.connect(config['name'], config['pw'])
            while not sta_if.isconnected():
                sleep(2)
    
    print('network::config:', sta_if.ifconfig())


def network_disconnect():
    import network
    
    network.WLAN(network.STA_IF).disconnect()


def ntp_time_sync():
    import ntptime
    from utime import sleep, localtime
    
    time_set = False
    while not time_set:
        try:
            print('ntp_sync::fetching')
            ntptime.settime()
            time_set = True
        except Exception as e:
            print('ntp_sync::except:', str(e))
            sleep(2)
        print('ntp_sync::utc:', str(localtime()))
