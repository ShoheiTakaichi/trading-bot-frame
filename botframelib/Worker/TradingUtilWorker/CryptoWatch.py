import json

import requests

from botframelib.EventSourcing import IWorker
from botframelib.Event.TradingEvent import *

API_CALL_INTERVAL = 3


class CryptoWatch(IWorker):
    def __init__(self):
        IWorker.__init__(self)

    def preprocess(self):
        return

    def getOhlcv(self, market: str, currency: str):
        query: dict[str, str] = {}
        url = "https://api.cryptowat.ch/markets/" + market + "/" + currency + "/ohlc"
        ohlcvs = json.loads(requests.get(url, query).text)
        return ohlcvs

    def onRunEveryMin(self, event):
        minutes = event.getData()["data"] // 60
        print(minutes)
        if minutes % API_CALL_INTERVAL == 0:
            ohlcvs = self.getOhlcv(market="liquid", currency="btcusdt")
            event = GetOhlcv({"data": ohlcvs})
