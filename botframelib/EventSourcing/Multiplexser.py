from datetime import datetime
from queue import Queue
from threading import Thread


class Multiplexer(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.eventStory = Queue()
        self.workers = []

    def addWorker(self, worker):
        self.workers.append(worker)
        worker.setEventstory(self.eventStory)

    def run(self):
        for worker in self.workers:
            worker.start()
        while True:
            event = self.eventStory.get()
            event.replication_time = datetime.now()
            for worker in self.workers:
                worker.taskQueue.put(event)
