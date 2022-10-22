import uuid
import ccxws
from loguru import logger

from botframelib.EventSourcing import IWorker
from botframelib.Event.TradingEvent import *


class WsSender(IWorker):
    def __init__(self, client, name: str):
        IWorker.__init__(self)
        self.client = client
        self.name = name
        self.isSOD = True
        self.id_map: dict[uuid.UUID, str] = {}

    def preprocess(self):
        self.client.start()

    def run(self):
        self.preprocess()
        while True:
            message = self.client.message_queue.get()
            event_name = type(message).__name__
            try:
                if event_name == "simple_orderbook":
                    if self.isSOD:
                        data = SODOrderBook(orderbook=message)
                        self.eventStory.put(data)
                        self.isSOD = False

                    data = UpdateOrderBook(orderbook=message)
                    self.eventStory.put(data)

                elif event_name == "execution":
                    data: ccxws.models.execution = message
                    event = UpdateExecution(execution=data)
                    self.eventStory.put(event)

                elif event_name == "user_execution":
                    try:
                        data: ccxws.models.user_execution = message
                        data.order_id = self._get_inner_id_by_external_id(data.order_id)
                        logger.info(data)
                        event = UpdateUserExecution(
                            wsengine_name=self.name, user_execution=data
                        )
                        self.eventStory.put(event)
                        self.id_map.pop(data.order_id)
                        self.eventStory.put(UpdateIdMap(id_map=self.id_map))
                    except Exception as e:
                        logger.error(e)

                elif event_name == "simple_user_order_list":
                    event = UpdateUserOrder(
                        wsengine_name=self.name, user_order_list=message
                    )
                    self.eventStory.put(event)
                else:
                    print("unhandled event" + event_name)

            except Exception as e:
                # print(traceback.format_exc())
                print("unexpected format in {}".format(event_name))
                print(e)
                print(message)

    def onUpdateIdMap(self, event: UpdateIdMap):
        """receriverとid_mapを同期する。"""
        self.id_map = event.id_map

    def _get_inner_id_by_external_id(self, external_id: str) -> uuid.UUID:
        inner_ids_as_list = list(self.id_map.keys())
        externel_ids_as_list = list(self.id_map.values())
        return inner_ids_as_list[externel_ids_as_list.index(external_id)]
