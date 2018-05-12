from machine import Timer


class Scheduler:
    
    def __init__(self, job):
        self.simple_job = lambda t: job()
        self.timer = None
    
    def start(self):
        if self.timer is None:
            self.timer = Timer(1)
            self.timer.init(period=500, mode=Timer.PERIODIC, callback=self.simple_job)
    
    def stop(self):
        if self.timer is not None:
            self.timer.deinit()
            self.timer = None
