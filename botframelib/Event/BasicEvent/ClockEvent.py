import uuid
from datetime import datetime
from botframelib.EventSourcing import IEvent


class RunEveryMin(IEvent):
    pass


class Every30Sec(IEvent):
    time: datetime


class EveryMinute(IEvent):
    time: datetime


class CreateCustomInterval(IEvent):
    id: uuid.UUID
    interval: float


class StopCustomInterval(IEvent):
    id: uuid.UUID


class CreateCustomIntervalWithOffset(IEvent):
    id: uuid.UUID
    interval: float
    offset: float


class CustomInterval(IEvent):
    id: uuid.UUID
    time: float
    interval: float


class SetTimer(IEvent):
    id: uuid.UUID
    time: float


class Timer(IEvent):
    id: uuid.UUID
    time: float
