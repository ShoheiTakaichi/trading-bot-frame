import time as t
import traceback
import uuid

from botframelib.EventSourcing import IWorker
from botframelib.Event.TradingEvent import *
from loguru import logger


class WsReceiver(IWorker):
    def __init__(self, client, name: str):
        IWorker.__init__(self)
        self.client = client
        self.name = name
        self.id_map: dict[uuid.UUID, str] = {}

    def onCreateMarketOrder(self, event: CreateMarketOrder):
        if event.wsengine_name == self.name:
            try:
                print("receiver onCreateMarketOrder", event, self.name, t.time())
                # self.client.create_market_order(
                #     symbol = event.symbol,
                #     amount = event.amount,
                #     side = event.side
                # )
            except Exception as e:
                logger.error(traceback.format_exc())

    def onCreateLimitOrder(self, event: CreateLimitOrder):
        if event.wsengine_name == self.name:
            try:
                res = self.client.create_order(
                    symbol=event.symbol,
                    amount=event.amount,
                    price=event.price,
                    side=event.side,
                )
                self.id_map[event.id_] = res["id"]
                self.eventStory.put(UpdateIdMap(id_map=self.id_map))
            except Exception as e:
                logger.error(traceback.format_exc())

    def onEditOrder(self, event: EditOrder):
        if event.wsengine_name == self.name:
            try:
                res = self.client.edit_order(
                    id=self.id_map[event.id_],
                    symbol=event.symbol,
                    amount=event.amount,
                    price=event.price,
                    side=event.side,
                )
                # editすると取引所側のidも更新されるのでmapも更新
                self.id_map[event.id_] = res["id"]
                self.eventStory.put(UpdateIdMap(id_map=self.id_map))
            except Exception as e:
                logger.error(traceback.format_exc())

    def onCancelOrder(self, event: CancelOrder):
        if event.wsengine_name == self.name:
            try:
                self.client.cancel_order(
                    id=self.id_map[event.id_],
                    symbol=event.symbol,
                )
                self.id_map.pop(event.id_)
                self.eventStory.put(UpdateIdMap(id_map=self.id_map))
            except Exception as e:
                logger.error(traceback.format_exc())

    def onCancelAllOrder(self, event: CancelOrder):
        if event.wsengine_name == self.name:
            try:
                orders = self.client.fetch_open_orders(symbol=event.symbol)
                logger.info(f"{orders}")
                for o in orders:
                    self.client.cancel_order(
                        symbol = event.symbol,
                        id = o["id"])
                self.id_map = {}
                self.eventStory.put(UpdateIdMap(id_map=self.id_map))
            except Exception as e:
                logger.error(f"{traceback.format_exc()}")

    def onCreateOrder(self, event: CreateOrder):
        # print('dry_run {} {}'.format(event.price, event.amount))
        if event.wsengine_name == self.name:
            try:
                res = self.client.create_order(
                    symbol=event.symbol,
                    side=event.side,
                    amount=event.amount,
                    price=event.price,
                )
                self.id_map[event.id_] = res["id"]
                self.eventStory.put(UpdateIdMap(id_map=self.id_map))
                self.eventStory.put(
                    CreateOrderInfo(
                        wsengine_name=event.wsengine_name,
                        price=event.price,
                        amount=event.amount,
                        side=event.side,
                    )
                )
            except Exception as e:
                logger.error(traceback.format_exc())

    def onRequestBalance(self, event):
        try:
            res = self.client.fetch_balance()
            self.eventStory.put(UpdateBalance(wsengine_name=self.name, balance=res))
            return res
        except Exception as e:
            logger.error(e)

    def onSubscribeSymbol(self, event: SubscribeSymbol):
        if event.wsengine_name == self.name:
            # # SODで呼ばれたときのみSODBalanceを取得
            # if event.isSOD:
            #     res_order_book = self.client.fetch_order_book(event.symbol)
            #     self.eventStory.put(SODOrderBook(
            #         orderbook=simple_orderbook(
            #             exchange=event.wsengine_name,
            #             symbol=res_order_book.symbol,

            #         )
            #     ))

            self.client.subscribe_orderbook(event.symbol)
            self.client.subscribe_execution(event.symbol)
            self.eventStory.put(
                UpdateOhlcv1min(
                    exchange=self.client.exchange,
                    symbol=event.symbol,
                    ohlcv=self.client.fetch_ohlcv(symbol=event.symbol, timeframe="1m"),
                )
            )
            self.eventStory.put(
                UpdateOhlcv1day(
                    exchange=self.client.exchange,
                    symbol=event.symbol,
                    ohlcv=self.client.fetch_ohlcv(symbol=event.symbol, timeframe="1d"),
                )
            )

    def onSODEvent(self, event):
        res = self.onRequestBalance(event)
        if res is not None:
            self.eventStory.put(SODBalance(wsengine_name=self.name, balance=res))

    def onEvery30Sec(self, event):
        self.onRequestBalance(event)

    def onUpdateIdMap(self, event: UpdateIdMap):
        """senderとid_mapを同期する。"""
        self.id_map = event.id_map
