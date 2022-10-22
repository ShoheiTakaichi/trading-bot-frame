from datetime import datetime
import uuid

from ccxws import models

from botframelib.EventSourcing import IEvent


class SODEvent(IEvent):
    time: datetime


class SODRequestInitialBalance(IEvent):
    wsengine_name: str


class SODBalance(IEvent):
    wsengine_name: str
    balance: models.balance


class SODOrderBook(IEvent):
    orderbook: models.simple_orderbook


class SODRequestOHLCV(IEvent):
    symbol: str
    timeframe: str


class EODEvent(IEvent):
    time: datetime


class EODSummary(IEvent):
    wsengine_name: str
    date: datetime
    totalVolume: float
    SODBalance: models.balance
    EODBalance: models.balance


class GetOhlcv(IEvent):
    pass


class RequestBalance(IEvent):
    data: str  # exchange


class SubscribeSymbol(IEvent):
    wsengine_name: str
    symbol: str
    isSOD: bool = False


class UpdateTotalVolume(IEvent):
    totalVolume: float


class CompactionCandle(IEvent):
    exchange: str
    symbol: str
    time: float
    open: float
    high: float
    low: float
    close: float
    volume: float


class UpdateIdMap(IEvent):
    id_map: dict[uuid.UUID, str]
