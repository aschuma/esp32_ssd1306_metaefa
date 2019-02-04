from machine import Timer


def default(job):
    return Scheduler(job=job, period=500)


class Scheduler:
    
    def __init__(self, job, period):
        self.simple_job = lambda t: job()
        self.timer = None
        self.period = period
    
    def start(self):
        if self.timer is None:
            self.timer = Timer(-1)
            self.timer.init(period=self.period, mode=Timer.PERIODIC, callback=self.simple_job)
        return self
    
    def stop(self):
        if self.timer is not None:
            self.timer.deinit()
            self.timer = None
        return self
