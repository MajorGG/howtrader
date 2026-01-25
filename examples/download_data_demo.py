import sys
from time import sleep
from datetime import datetime, time, timedelta
from logging import INFO

from howtrader.event import EventEngine
from howtrader.trader.setting import SETTINGS
from howtrader.trader.engine import MainEngine

from howtrader.gateway.binance import BinanceUsdtGateway, BinanceSpotGateway
from howtrader.trader.object import Exchange, Interval, BarData
from howtrader.trader.object import HistoryRequest
from howtrader.trader.database import BaseDatabase, get_database

database: BaseDatabase = get_database()

from threading import Thread

SETTINGS["log.active"] = True
SETTINGS["log.level"] = INFO
SETTINGS["log.console"] = True

usdt_gateway_setting = {
    "key": "mZoncCNtXIwQ8X6HQ0489GHyKqTdCXLLvhRTlmC7jCJGyR7qMmpoOlWuMMzOnwO0",
    "secret": "pqTMvnf81J1xBVYzA3x1BxKjdST8NMEtaprYtyfDmrscVj1hcUL7FPcBAbHdry4z",
    "proxy_host": "127.0.0.1",
    "proxy_port": 0
}

if __name__ == "__main__":

    # exchange = Exchange.BINANCE  # binance.
    # interval = Interval.MINUTE_15  # minute
    # symbol = "BTCUSDT"
    #
    # start = datetime(2025, 2, 1)
    # end = datetime(2025, 2, 15)
    #
    # data: [BarData] = database.load_bar_data(symbol, exchange, interval, start, end)
    # print(len(data))

    """
        for crawling data from Binance exchange.
    """
    SETTINGS["log.file"] = True

    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)

    main_engine.add_gateway(BinanceUsdtGateway)  # future
    main_engine.add_gateway(BinanceSpotGateway)  # spot

    # main_engine.connect(usdt_gateway_setting, "BINANCE_SPOT")  # spot
    main_engine.connect(usdt_gateway_setting, "BINANCE_USDT")  # future
    sleep(5)

    # gate_way = main_engine.get_gateway("BINANCE_SPOT")  # spot
    gate_way = main_engine.get_gateway("BINANCE_USDT")  # future
    # print(gate_way)

    # symbol = "BTCUSDT"
    # symbol = "btcusdt"
    symbol = "ETHUSDT"
    # symbol = "ETHBTC"
    # symbol = "ethusdt"  # spot for lower case while the future will be upper case.

    exchange = Exchange.BINANCE  # binance.
    interval = Interval.MINUTE_15  # minute

    # start = datetime(2025, 12, 20)
    start = datetime.now() - timedelta(days=30)
    # end = datetime(2025, 2, 15)
    req = HistoryRequest(
        symbol=symbol,
        exchange=exchange,
        interval=interval,
        start=start,
        # end=end
    )

    # bars = gate_way.open_interest_hist(req)
    # print(len(bars))

    # req.start = datetime.now() - timedelta(days=30)
    # bars = gate_way.global_long_short_account_ratio(req)
    # print(len(bars))
    # print(database.save_global_long_short_account_ratio(bars))
    #
    # req.start = datetime.now() - timedelta(days=30)
    # bars = gate_way.taker_long_short_ratio(req)
    # print(len(bars))
    # print(database.save_taker_long_short_ratio(bars))
    #
    # req.start = datetime.now() - timedelta(days=30)
    # bars = gate_way.top_long_short_account_ratio(req)
    # print(len(bars))
    # print(database.save_top_long_short_account_ratio(bars))

    req.start = datetime.now() - timedelta(days=30)
    bars = gate_way.top_long_short_position_ratio(req)
    print(len(bars))
    print(database.save_top_long_short_position_ratio(bars))

    req.start = datetime.now() - timedelta(days=30)
    req.interval = Interval.MINUTE_5
    bars = gate_way.top_long_short_position_ratio(req)
    print(len(bars))
    print(database.save_top_long_short_position_ratio(bars))

    print('success')
    # am = ArrayManager()
    # for v in bars:
    #     am.update_bar(v)
    # print(am)
    #
    # sar_value = talib.SAR(am.high_array, am.low_array)
    #
    # print("value", am.high_array, am.low_array)
    # print("SAR", sar_value)
    #
    # for i in range(100):
    #     print(f'{am.high_array[i]}-{am.low_array[i]}-{am.close_array[i]}-{sar_value[i]}')
