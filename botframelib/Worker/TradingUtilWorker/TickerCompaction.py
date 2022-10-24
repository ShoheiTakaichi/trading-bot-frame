import time as t

from botframelib.EventSourcing import IWorker
from botframelib.Event.TradingEvent import *


class TickerCompaction(IWorker):
    def __init__(self):
        IWorker.__init__(self)
        self.candleStick = {}
        self.timestamp = t.time() // 60 * 60
        self.isStart = False

    def onEveryMinute(self, event):
        self.timestamp = t.time() // 60 * 60
        if not self.isStart:
            self.isStart = True
            return
        for k in self.candleStick.keys():
            self.eventStory.put(self.candleStick[k])
            self.candleStick[k] = CompactionCandle(
                exchange=self.candleStick[k].exchange,
                symbol=self.candleStick[k].symbol,
                time=self.timestamp,
                open=self.candleStick[k].open,
                high=self.candleStick[k].high,
                low=self.candleStick[k].low,
                close=self.candleStick[k].close,
                volume=0,
            )

    def onUpdateExecution(self, event):
        execution = event.execution
        exchange = execution.exchange
        symbol = execution.symbol
        if exchange + symbol not in self.candleStick.keys():
            self.candleStick[exchange + symbol] = CompactionCandle(
                exchange=exchange,
                symbol=symbol,
                time=self.timestamp,
                open=execution.price,
                high=execution.price,
                low=execution.price,
                close=execution.price,
                volume=execution.amount * execution.price,
            )
        else:
            if self.candleStick[exchange + symbol].volume == 0:
                self.candleStick[exchange + symbol] = CompactionCandle(
                    exchange=exchange,
                    symbol=symbol,
                    time=self.timestamp,
                    open=execution.price,
                    high=execution.price,
                    low=execution.price,
                    close=execution.price,
                    volume=execution.amount * execution.price,
                )
            else:
                self.candleStick[exchange + symbol] = CompactionCandle(
                    exchange=exchange,
                    symbol=symbol,
                    time=self.timestamp,
                    open=self.candleStick[exchange + symbol].open,
                    high=max(execution.price, self.candleStick[exchange + symbol].high),
                    low=min(execution.price, self.candleStick[exchange + symbol].low),
                    close=execution.price,
                    volume=self.candleStick[exchange + symbol].volume
                    + execution.amount * execution.price,
                )
