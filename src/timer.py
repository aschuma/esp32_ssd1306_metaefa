from machine import Timer


def daily(job, id=1):
    return Scheduler(job=job, id=id, period=1000 * 60 * 60 * 24)


def default(job, id=2):
    return Scheduler(job=job, id=id, period=500)


class Scheduler:
    
    def __init__(self, job, id, period):
        self.simple_job = lambda t: job()
        self.timer = None
        self.id = id
        self.period = period
    
    def start(self):
        if self.timer is None:
            self.timer = Timer(self.id)
            self.timer.init(period=self.period, mode=Timer.PERIODIC, callback=self.simple_job)
    
    def stop(self):
        if self.timer is not None:
            self.timer.deinit()
            self.timer = None
