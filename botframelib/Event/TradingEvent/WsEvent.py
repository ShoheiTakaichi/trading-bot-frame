import uuid
from typing import List

from ccxws import models

from botframelib.EventSourcing import IEvent
from .Models import Order


class UpdateOrderBook(IEvent):
    orderbook: models.simple_orderbook


class UpdateExecution(IEvent):
    execution: models.execution


class UpdateUserExecution(IEvent):
    wsengine_name: str
    user_execution: models.user_execution


class UpdateUserOrder(IEvent):
    wsengine_name: str
    user_order_list: models.simple_user_order_list


class UpdateBalance(IEvent):
    wsengine_name: str
    balance: models.balance


class CreateLimitOrder(IEvent):
    id_: uuid.UUID
    wsengine_name: str
    symbol: str
    side: str
    amount: float
    price: float


class CreateOrder(IEvent):
    wsengine_name: str
    id_: uuid.UUID
    symbol: str
    price: float
    side: str
    amount: float


class CreateMarketOrder(IEvent):
    wsengine_name: str
    symbol: str
    side: str
    amount: float


class CreateOrderInfo(IEvent):
    wsengine_name: str
    price: float
    amount: float
    side: str


class EditOrder(IEvent):
    id_: uuid.UUID
    wsengine_name: str
    symbol: str
    side: str
    amount: float
    price: float


class EditOrderInfo(IEvent):
    wsengine_name: str


class CancelOrder(IEvent):
    id_: uuid.UUID
    wsengine_name: str
    symbol: str


class CancelAllOrder(IEvent):
    wsengine_name: str
    symbol: str


class CancelOrderInfo(IEvent):
    wsengine_name: str


class UpdateOhlcv1min(IEvent):
    exchange: str
    symbol: str
    ohlcv: list[list]

class UpdateOhlcv5min(IEvent):
    exchange: str
    symbol: str
    ohlcv: list[list]

class UpdateOhlcv1hour(IEvent):
    exchange: str
    symbol: str
    ohlcv: list[list]

class UpdateOhlcv1day(IEvent):
    exchange: str
    symbol: str
    ohlcv: list[list]
