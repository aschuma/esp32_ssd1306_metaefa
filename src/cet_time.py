try:
    import utime
    
    
    def _mkd(year, month, day, h, m, s):
        return utime.mktime((year, month, day, h, m, s, 0, 0))
    
    
    _utc_transition_ts = [
        _mkd(2000, 3, 26, 1, 0, 0),
        _mkd(2000, 10, 29, 1, 0, 0),
        _mkd(2001, 3, 25, 1, 0, 0),
        _mkd(2001, 10, 28, 1, 0, 0),
        _mkd(2002, 3, 31, 1, 0, 0),
        _mkd(2002, 10, 27, 1, 0, 0),
        _mkd(2003, 3, 30, 1, 0, 0),
        _mkd(2003, 10, 26, 1, 0, 0),
        _mkd(2004, 3, 28, 1, 0, 0),
        _mkd(2004, 10, 31, 1, 0, 0),
        _mkd(2005, 3, 27, 1, 0, 0),
        _mkd(2005, 10, 30, 1, 0, 0),
        _mkd(2006, 3, 26, 1, 0, 0),
        _mkd(2006, 10, 29, 1, 0, 0),
        _mkd(2007, 3, 25, 1, 0, 0),
        _mkd(2007, 10, 28, 1, 0, 0),
        _mkd(2008, 3, 30, 1, 0, 0),
        _mkd(2008, 10, 26, 1, 0, 0),
        _mkd(2009, 3, 29, 1, 0, 0),
        _mkd(2009, 10, 25, 1, 0, 0),
        _mkd(2010, 3, 28, 1, 0, 0),
        _mkd(2010, 10, 31, 1, 0, 0),
        _mkd(2011, 3, 27, 1, 0, 0),
        _mkd(2011, 10, 30, 1, 0, 0),
        _mkd(2012, 3, 25, 1, 0, 0),
        _mkd(2012, 10, 28, 1, 0, 0),
        _mkd(2013, 3, 31, 1, 0, 0),
        _mkd(2013, 10, 27, 1, 0, 0),
        _mkd(2014, 3, 30, 1, 0, 0),
        _mkd(2014, 10, 26, 1, 0, 0),
        _mkd(2015, 3, 29, 1, 0, 0),
        _mkd(2015, 10, 25, 1, 0, 0),
        _mkd(2016, 3, 27, 1, 0, 0),
        _mkd(2016, 10, 30, 1, 0, 0),
        _mkd(2017, 3, 26, 1, 0, 0),
        _mkd(2017, 10, 29, 1, 0, 0),
        _mkd(2018, 3, 25, 1, 0, 0),
        _mkd(2018, 10, 28, 1, 0, 0),
        _mkd(2019, 3, 31, 1, 0, 0),
        _mkd(2019, 10, 27, 1, 0, 0),
        _mkd(2020, 3, 29, 1, 0, 0),
        _mkd(2020, 10, 25, 1, 0, 0),
        _mkd(2021, 3, 28, 1, 0, 0),
        _mkd(2021, 10, 31, 1, 0, 0),
        _mkd(2022, 3, 27, 1, 0, 0),
        _mkd(2022, 10, 30, 1, 0, 0),
        _mkd(2023, 3, 26, 1, 0, 0),
        _mkd(2023, 10, 29, 1, 0, 0),
        _mkd(2024, 3, 31, 1, 0, 0),
        _mkd(2024, 10, 27, 1, 0, 0),
        _mkd(2025, 3, 30, 1, 0, 0),
        _mkd(2025, 10, 26, 1, 0, 0),
        _mkd(2026, 3, 29, 1, 0, 0),
        _mkd(2026, 10, 25, 1, 0, 0),
        _mkd(2027, 3, 28, 1, 0, 0),
        _mkd(2027, 10, 31, 1, 0, 0),
        _mkd(2028, 3, 26, 1, 0, 0),
        _mkd(2028, 10, 29, 1, 0, 0),
        _mkd(2029, 3, 25, 1, 0, 0),
        _mkd(2029, 10, 28, 1, 0, 0),
        _mkd(2030, 3, 31, 1, 0, 0),
        _mkd(2030, 10, 27, 1, 0, 0),
        _mkd(2031, 3, 30, 1, 0, 0),
        _mkd(2031, 10, 26, 1, 0, 0),
        _mkd(2032, 3, 28, 1, 0, 0),
        _mkd(2032, 10, 31, 1, 0, 0),
        _mkd(2033, 3, 27, 1, 0, 0),
        _mkd(2033, 10, 30, 1, 0, 0),
        _mkd(2034, 3, 26, 1, 0, 0),
        _mkd(2034, 10, 29, 1, 0, 0),
        _mkd(2035, 3, 25, 1, 0, 0),
        _mkd(2035, 10, 28, 1, 0, 0),
        _mkd(2036, 3, 30, 1, 0, 0),
        _mkd(2036, 10, 26, 1, 0, 0),
        _mkd(2037, 3, 29, 1, 0, 0),
        _mkd(2037, 10, 25, 1, 0, 0)
    ]
    
    _one_hour_in_seconds = 60 * 60


    def _is_summer_time(sec_since_2000_input):
        count = 0
        for ts in _utc_transition_ts:
            if ts < sec_since_2000_input:
                count = count + 1
        return count % 2 == 1
    
    
    def mktime(year, month, day, hour, minute):
        utc_ts = utime.mktime((year, month, day, hour, minute, 0, 0, 0))
        offset = 2 if _is_summer_time(utime.time()) else 1
        return utc_ts - offset * _one_hour_in_seconds
    
    
    def now():
        now_utc = utime.time()
        offset = 2 if _is_summer_time(now_utc) else 1
        
        return utime.localtime(now_utc + _one_hour_in_seconds * offset)


except:
    import time
    
    
    def mktime(year, month, day, hour, minute):
        return int(time.mktime((year, month, day, hour, minute, 0, 0, 0, 0)))
    
    
    def now():
        record = time.localtime()
        return (record.tm_year,
                record.tm_mon,
                record.tm_mday,
                record.tm_hour,
                record.tm_min,
                record.tm_sec,
                0,
                record.tm_yday)


def current_time_formatted():
    date_time = now()
    return '{:02d}:{:02d}:{:02d}'.format(date_time[3], date_time[4], date_time[5])
