import utime


def _is_summer_time(sec_since_2000):
    summer_times = [
        (1521943200, 1540695600),
        (1553997600, 1572145200),
        (1585447200, 1603594800)
    ]

    sec_2000 = 946684800

    for interval in summer_times:
        if interval[0] <= (sec_since_2000 + sec_2000) <= interval[1]:
            return True

    return False


def current():
    one_hour_in_seconds = 60 * 60
    now_utc = utime.mktime(utime.localtime())

    if _is_summer_time(now_utc):
        offset = 2
    else:
        offset = 1

    return utime.localtime(now_utc + one_hour_in_seconds * offset)

