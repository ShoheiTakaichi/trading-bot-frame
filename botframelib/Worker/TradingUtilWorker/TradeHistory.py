from botframelib.EventSourcing import IWorker
from botframelib.Event.TradingEvent import *


class TradeHistory(IWorker):
    def __init__(self):
        IWorker.__init__(self)

    def onSODEvent(self, event):
        self.totalVolume = 0

    def onEveryMinute(self, event):
        pass

    def onUpdateUserExecution(self, event: UpdateUserExecution):
        userexecution = event.user_execution
        if userexecution.taker_side == userexecution.my_side:
            self.totalVolume += userexecution.price * userexecution.amount
            self.eventStory.put(UpdateTotalVolume(totalVolume=self.totalVolume))
