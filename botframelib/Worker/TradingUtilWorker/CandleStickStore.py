from loguru import logger

from botframelib.EventSourcing import IWorker
from botframelib.Event.TradingEvent import *

class CandleStickStore(IWorker):
    def __init__(self):
        IWorker.__init__(self)
        data = {}

    def onUpdateOhlcv1min(self, event):
        logger.info(f"{event}")
        
    def onCompactionCandle(self, event):
        logger.info(f"{event}")

'''
Signal.Signal:onUpdateOhlcv1min:26 - 
creation_time=datetime.datetime(2022, 10, 25, 5, 2, 37, 155158) 
replication_time=datetime.datetime(2022, 10, 25, 5, 2, 42, 323748) 
exchange='bitflyer' 
symbol='BTC/JPY' 
ohlcv=[
    [1666673100000, 2879192.0, 2879192.0, 2878800.0, 2878801.0, 0.23000000000000007],
    [1666673160000, 2878801.0, 2878801.0, 2878801.0, 2878801.0, 0.049], 
    [1666673220000, 2878801.0, 2878801.0, 2878801.0, 2878801.0, 0.0173], 
    [1666673280000, 2878801.0, 2878888.0, 2878801.0, 2878888.0, 0.013179999999999999], 
    [1666673340000, 2878891.0, 2878891.0, 2878891.0, 2878891.0, 0.01], 
    [1666673520000, 2878891.0, 2878901.0, 2878891.0, 2878901.0, 0.08], 
    [1666673580000, 2878928.0, 2878928.0, 2878928.0, 2878928.0, 0.03], 
    [1666673640000, 2878928.0, 2879851.0, 2878928.0, 2878928.0, 0.13110999999999998], 
    [1666673700000, 2878928.0, 2881212.0, 2878928.0, 2880842.0, 3.099999999999999], 
    [1666673760000, 2880811.0, 2880811.0, 2880811.0, 2880811.0, 0.001], 
    [1666673820000, 2880917.0, 2881662.0, 2880917.0, 2881001.0, 0.48], 
    [1666673940000, 2881001.0, 2881001.0, 2881001.0, 2881001.0, 0.0424], 
    [1666674000000, 2881001.0, 2881313.0, 2880500.0, 2880641.0, 0.10919999999999998], 
    [1666674060000, 2880641.0, 2880641.0, 2880641.0, 2880641.0, 0.013600000000000001]]
    [1666674180.0 , 2888403.0, 2888095.0, 2888124.0, 2929234.26362145]

Signal.Signal:onCompactionCandle:23 - 
creation_time=datetime.datetime(2022, 10, 25, 5, 2, 37, 155158) 
replication_time=datetime.datetime(2022, 10, 25, 5, 4, 0, 26780) 
exchange='bitflyer' 
symbol='FX_BTC_JPY' 
time=1666674180.0 
open=2888403.0 
high=2888825.0 
low=2888095.0 
close=2888124.0 
volume=2929234.26362145


'''
