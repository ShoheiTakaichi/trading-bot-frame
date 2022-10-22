import uuid

from ccxws import mexc

from botframelib import *
from botframelib import BasicEvent



mexc = mexc(apiKey=api, secret=secret)

multiplexer = Multiplexer()

WorkerList = [
    Clock(),
    CustomClock(),
    EventLogger(),
    # WsSender(mexc, "mexc_1"),
    # WsReceiver(mexc, "mexc_1"),
    # SOD({"mexc_1": ["BTC/USDT"]}),
]

a = list(map(multiplexer.addWorker, WorkerList))

multiplexer.start()

import time

time.sleep(1)
# multiplexer.eventStory.put(SODStart(time=time.time()))
