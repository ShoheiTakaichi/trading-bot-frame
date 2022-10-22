from botframelib.EventSourcing import IWorker
from botframelib.Event.TradingEvent import *


class SOD(IWorker):
    def __init__(self, engine_symbols_dict: dict[str, list[str]]):
        IWorker.__init__(self)
        self.engine_symbols_dict = engine_symbols_dict

    def onSODEvent(self, event: SODEvent):
        for engine, symbols in self.engine_symbols_dict.items():
            for symbol in symbols:
                self.eventStory.put(
                    SubscribeSymbol(wsengine_name=engine, symbol=symbol, isSOD=True)
                )
