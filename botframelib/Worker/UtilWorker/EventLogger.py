from datetime import datetime
from pathlib import Path

from loguru import logger

from botframelib.EventSourcing import IWorker


class EventLogger(IWorker):
    def __init__(self, log_file=None):
        IWorker.__init__(self)
        self.log_file = log_file

    def onEventLogger(self, event):
        if self.log_file is None:
            if event.__class__.__name__ not in ['UpdateExecution', 'UpdateOrderBook']:
                logger.info(f"{event.__class__.__name__}")
                # logger.info(f"{event}")
        else:
            Path(self.log_file).touch(exist_ok=True)
            with open(self.log_file, "a") as f:
                print(f"{event.__class__.__name__} {event}", file=f)

    def eventHandler(self, event):
        self.onEventLogger(event)
