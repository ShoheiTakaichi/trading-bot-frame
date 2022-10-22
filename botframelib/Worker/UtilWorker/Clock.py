import time
from datetime import datetime
from botframelib.Event import *
from botframelib.EventSourcing import IWorker


class Clock(IWorker):
    def __init__(self):
        IWorker.__init__(self)

    def run(self):
        while True:
            wait_time = 60 - (time.time() % 60)
            time.sleep(wait_time)
            now = datetime.utcnow()
            if now.hour == 0 and now.minute == 0:
                self.eventStory.put(EODEvent(time=now))
                self.eventStory.put(SODEvent(time=now))
            self.eventStory.put(EveryMinute(time=now))
            self.eventStory.put(Every30Sec(time=now))
            time.sleep(30 - (time.time() % 30))
            self.eventStory.put(Every30Sec(time=datetime.utcnow()))
            time.sleep(1)