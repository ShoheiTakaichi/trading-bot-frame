import time as t

from botframelib.EventSourcing import IWorker
from botframelib.Event.TradingEvent import *


class CandleStickCompaction(IWorker):
    def __init__(self):
        IWorker.__init__(self)
        self.candleStick = {}
        self.timestamp = t.time() // 60 * 60
        self.isStart = False

    def onCompactionCandle(self, event):
        if event.exchange + event.symbol in self.candleStick.keys():
            self.candleStick[event.exchange + event.symbol].high = max(event.high, self.candleStick[event.exchange + event.symbol].high)
            self.candleStick[event.exchange + event.symbol].low = min(event.low, self.candleStick[event.exchange + event.symbol].low )
            self.candleStick[event.exchange + event.symbol].close = event.close
            self.candleStick[event.exchange + event.symbol].volume += event.volume 
            if self.event.time % 300 // 60 == 4:
                self.eventstory.put(
                    self.candleStick.pop(event.exchange + event.symbol)
                )
        else:
            if self.event.time % 300 // 60 == 0:
                self.candleStick[event.exchange + event.symbol] = CompactionCandle5min(
                    exchange=event.exchange,
                    symbol=sevent.symbol,
                    time=event.timestamp,
                    open=event.open,
                    high=event.high,
                    low=event.low,
                    close=event.close,
                    volume=event.volume,
                )