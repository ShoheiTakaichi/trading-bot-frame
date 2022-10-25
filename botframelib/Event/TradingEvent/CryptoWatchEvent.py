import uuid
from typing import List

from ccxws import models
import pandas as pd

from botframelib.EventSourcing import IEvent
from .Models import Order

class CryptoWatchEvent(IEvent):
    exchange: str
    symbol: str

class CryptoWatch1min(IEvent):
    exchange: str
    symbol: str
    ohlcv: pd.DataFrame

class CryptoWatch3min(IEvent):
    exchange: str
    symbol: str
    ohlcv: list[list]

class CryptoWatch5min(IEvent):
    exchange: str
    symbol: str
    ohlcv: pd.DataFrame

class CryptoWatch15min(IEvent):
    exchange: str
    symbol: str
    ohlcv: pd.DataFrame
    ohlcv: list[list]

class CryptoWatch30min(IEvent):
    exchange: str
    symbol: str
    ohlcv: pd.DataFrame

class CryptoWatch1hour(IEvent):
    exchange: str
    symbol: str
    ohlcv: pd.DataFrame

class CryptoWatch2hour(IEvent):
    exchange: str
    symbol: str
    ohlcv: pd.DataFrame

class CryptoWatch4hour(IEvent):
    exchange: str
    symbol: str
    ohlcv: pd.DataFrame

class CryptoWatch6hour(IEvent):
    exchange: str
    symbol: str
    ohlcv: pd.DataFrame

class CryptoWatch1d(IEvent):
    exchange: str
    symbol: str
    ohlcv: pd.DataFrame

class CryptoWatch3d(IEvent):
    exchange: str
    symbol: str
    ohlcv: pd.DataFrame

class CryptoWatch7d(IEvent):
    exchange: str
    symbol: str
    ohlcv: pd.DataFrame

class CryptoWatch7dm(IEvent):
    exchange: str
    symbol: str
    ohlcv: pd.DataFrame