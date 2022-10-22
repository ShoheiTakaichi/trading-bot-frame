from botframelib.EventSourcing import IWorker
from botframelib.Event.TradingEvent import *


class RestSubscribe(IWorker):
    def __init__(self):
        IWorker.__init__(self)

    def onEvery30Sec(self, event):
        self.eventStory.put(RequestBalance({}))
