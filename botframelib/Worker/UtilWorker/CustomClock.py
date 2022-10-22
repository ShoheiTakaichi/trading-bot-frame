import threading
import time as t
from queue import PriorityQueue, Queue
from threading import Thread

from pydantic import BaseModel

from botframelib.Event.BasicEvent import *
from botframelib.EventSourcing import IWorker


class CustomClock(IWorker):
    def __init__(self):
        IWorker.__init__(self)
        self.timer = InnerClock()
        self.timer.start()

    def setEventstory(self, eventStory):
        self.eventStory = eventStory
        self.timer.eventStory = eventStory

    def onCreateCustomInterval(self, event: CreateCustomInterval):
        self.timer.setInterval(event.id, event.interval)

    def onCreateCustomIntervalWithOffset(self, event: CreateCustomIntervalWithOffset):
        self.timer.setIntervalWithOffset(event.id, event.interval, event.offset)

    def onStopCustomInterval(self, event: StopCustomInterval):
        if event.id in self.timer.intervalList:
            self.timer.intervalList.remove(event.id)

    def onSetTimer(self, event: SetTimer):
        self.timer.setTimer(event.id, event.time)


class InnerClock(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.next = PriorityQueue()
        self.eventStory = Queue()
        self.newInterval = threading.Event()
        self.intervalList = []

    def run(self):
        while True:
            T = self.next.get()
            toWait = T.time - t.time()
            if toWait <= 0:

                if not T.once:
                    # イベント発行
                    self.eventStory.put(
                        CustomInterval(id=T.id, time=T.time, interval=T.interval)
                    )
                    if T.id in self.intervalList:
                        T.time += T.interval
                        self.next.put(T)
                if T.once:
                    self.eventStory.put(Timer(id=T.id, time=T.time))
                    self.intervalList.remove(T.id)
            if toWait > 0:
                self.newInterval.wait(toWait)
                self.next.put(T)
                self.newInterval.clear()

    def setInterval(self, id: uuid.UUID, interval: float):
        if id not in self.intervalList:
            self.intervalList.append(id)
            self.next.put(
                Interval(id=id, time=t.time() + interval, interval=interval, once=False)
            )
            self.newInterval.set()

    def setIntervalWithOffset(self, id: uuid.UUID, interval: float, offset: int):
        if id not in self.intervalList:
            self.intervalList.append(id)
            self.next.put(
                Interval(id=id, time=t.time() + offset, interval=interval, once=False)
            )
            self.newInterval.set()

    def setTimer(self, id: uuid.UUID, time: float):
        if id not in self.intervalList:
            self.intervalList.append(id)
            self.next.put(Interval(id=id, time=time, interval=10000, once=True))
            self.newInterval.set()


class Interval(BaseModel):
    id: uuid.UUID
    time: float
    interval: float
    once: bool

    def __lt__(self, other):
        return self.time < other.time

    def __le__(self, other):
        return self.time <= other.time

    def __gt__(self, other):
        return self.time > other.time

    def __ge__(self, other):
        return self.time >= other.time
