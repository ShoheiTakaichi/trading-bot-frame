import json

import requests
import pandas as pd

from botframelib.EventSourcing import IWorker
from botframelib.Event.TradingEvent import *


class CryptoWatch(IWorker):
    def __init__(self):
        IWorker.__init__(self)

    def onCryptoWatch(self, Event: CryptoWatchEvent):
        exchange = Event.exchange
        symbol = Event.symbol
        try:
            query: dict[str, str] = {}
            url = "https://api.cryptowat.ch/markets/" + exchange + "/" + symbol + "/ohlc"
            ohlcvs = json.loads(requests.get(url, query).text)
            for k in ohlcvs["result"].keys():
                df = pd.DataFrame(ohlcvs["result"][k], columns=['timestamp','open','high','low','close','amount','volume'])
                df['timestamp'] = pd.to_datetime(df['timestamp'].astype(int), unit='s')
                if k == '60':
                    self.eventStory.put(CryptoWatch1min(exchange=exchange, symbol=symbol, ohlcv=df))
                if k == '180':
                    self.eventStory.put(CryptoWatch3min(exchange=exchange, symbol=symbol, ohlcv=df))
                if k == '300':
                    self.eventStory.put(CryptoWatch5min(exchange=exchange, symbol=symbol, ohlcv=df))
                if k == '900':
                    self.eventStory.put(CryptoWatch15min(exchange=exchange, symbol=symbol, ohlcv=df))
                if k == '1800':
                    self.eventStory.put(CryptoWatch30min(exchange=exchange, symbol=symbol, ohlcv=df))
                if k == '3600':
                    self.eventStory.put(CryptoWatch1hour(exchange=exchange, symbol=symbol, ohlcv=df))
                if k == '7200':
                    self.eventStory.put(CryptoWatch2hour(exchange=exchange, symbol=symbol, ohlcv=df))
                if k == '14400':
                    self.eventStory.put(CryptoWatch4hour(exchange=exchange, symbol=symbol, ohlcv=df))
                if k == '21600':
                    self.eventStory.put(CryptoWatch6hour(exchange=exchange, symbol=symbol, ohlcv=df))
                if k == '43200':
                    self.eventStory.put(CryptoWatch12hour(exchange=exchange, symbol=symbol, ohlcv=df))
                if k == '86400':
                    self.eventStory.put(CryptoWatch1d(exchange=exchange, symbol=symbol, ohlcv=df))
                if k == '259200':
                    self.eventStory.put(CryptoWatch3d(exchange=exchange, symbol=symbol, ohlcv=df))
                if k == '604800':
                    self.eventStory.put(CryptoWatch7d(exchange=exchange, symbol=symbol, ohlcv=df))
                if k == '604800_Monday':
                    self.eventStory.put(CryptoWatch7dm(exchange=exchange, symbol=symbol, ohlcv=df))
        except:
            return