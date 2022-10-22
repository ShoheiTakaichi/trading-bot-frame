import inspect
import uuid
from queue import Queue
from threading import Thread

from loguru import logger


class IWorker(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.taskQueue = Queue()
        self.eventStory = Queue()
        self.workerId = uuid.uuid4()
        self.onEvents = list(
            filter(
                lambda x: x[0:2] == "on",
                map(lambda x: x[0], inspect.getmembers(self, inspect.ismethod)),
            )
        )

    def getWorkerId(self):
        return self.workerId

    def setEventstory(self, eventStory):
        self.eventStory = eventStory

    def eventHandler(self, event):
        event_name = event.__class__.__name__
        if "on" + event_name in self.onEvents:
            exec("self.on" + event_name + "(event)")
            # self.onEvent[type(event)](event)
            # event_name = event.__class__.__name__
            # ws_sender_events = ["UpdateOrderBook", "UpdateBalance"]
            # if event_name not in ws_sender_events:
            #     logger.info(f"[{self.__class__.__name__}] {event_name}")
        return

    def preprocess(self):
        return

    def run(self):
        self.preprocess()
        while True:
            event = self.taskQueue.get()
            self.eventHandler(event)

    def health_check(self):
        return True
