import uuid
import os
import time

import ccxws

from botframelib import EventSourcing, Worker, Event


symbol = "BTC/USDT"
exchange = "bitfinex"
client = ccxws.bitfinex(
    apiKey=os.environ.get("BITFINEX_API"), secret=os.environ.get("BITFINEX_SECRET")
)
multiplexer = EventSourcing.Multiplexer()

worker_list = [
    # Clock(),
    # CustomClock(),
    Worker.EventLogger(),
    Worker.WsSender(client, exchange),
    Worker.WsReceiver(client, exchange),
    Worker.SOD({exchange: [symbol]}),
]

list(map(multiplexer.addWorker, worker_list))

multiplexer.start()

time.sleep(1)
multiplexer.eventStory.put(Event.SODEvent(time=time.time()))
