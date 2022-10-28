from loguru import logger
import time as t

from botframelib.EventSourcing import IWorker
from botframelib.Event.TradingEvent import *


class CandleStickCompaction(IWorker):
    def __init__(self):
        IWorker.__init__(self)
        self.candleStick = {}
        self.isStart = False

    def onCompactionCandle(self, event):
        if event.exchange + event.symbol in self.candleStick.keys():
            self.candleStick[event.exchange + event.symbol].high = max(event.high, self.candleStick[event.exchange + event.symbol].high)
            self.candleStick[event.exchange + event.symbol].low = min(event.low, self.candleStick[event.exchange + event.symbol].low )
            self.candleStick[event.exchange + event.symbol].close = event.close
            self.candleStick[event.exchange + event.symbol].volume += event.volume 
            if event.time // 60 % 5 == 4:
                self.eventstory.put(
                    self.candleStick[event.exchange + event.symbol]
                )
            self.candleStick.pop(event.exchange + event.symbol)
        else:
            logger.info(event.time)
            if event.time // 60 % 5 == 0:
                self.candleStick[event.exchange + event.symbol] = CompactionCandle5min(
                    exchange=event.exchange,
                    symbol=event.symbol,
                    time=event.time,
                    open=event.open,
                    high=event.high,
                    low=event.low,
                    close=event.close,
                    volume=event.volume,
                )
            