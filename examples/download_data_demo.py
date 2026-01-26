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

def fetch_data(gate_way, database, symbol, exchange, interval, start):
    # symbol = "ETHUSDT"
    # # symbol = "ETHBTC"
    # # symbol = "ethusdt"  # spot for lower case while the future will be upper case.
    #
    # exchange = Exchange.BINANCE  # binance.
    # interval = Interval.MINUTE_15  # minute

    # start = datetime(2026, 1, 1)
    # start = datetime.now() - timedelta(days=30)
    # end = datetime(2025, 2, 15)
    req = HistoryRequest(
        symbol=symbol,
        exchange=exchange,
        interval=interval,
        start=start,
        # end=end
    )

    bars = gate_way.query_history(req)
    print(len(bars))
    database.save_bar_data(bars)

    bars = gate_way.open_interest_hist(req)
    print(len(bars))
    # database.delete_open_interest_hist(symbol, exchange)
    database.save_open_interest_hist(bars)

    # req.start = datetime.now() - timedelta(days=30)
    bars = gate_way.global_long_short_account_ratio(req)
    print(len(bars))
    # database.delete_global_long_short_account_ratio(symbol, exchange)
    database.save_global_long_short_account_ratio(bars)

    bars = gate_way.taker_long_short_ratio(req)
    print(len(bars))
    # database.delete_taker_long_short_ratio(symbol, exchange)
    database.save_taker_long_short_ratio(bars)

    bars = gate_way.top_long_short_account_ratio(req)
    print(len(bars))
    # database.delete_top_long_short_account_ratio(symbol, exchange)
    database.save_top_long_short_account_ratio(bars)

    # req.start = datetime.now() - timedelta(days=30)
    bars = gate_way.top_long_short_position_ratio(req)
    print(len(bars))
    # database.delete_top_long_short_position_ratio(symbol, exchange)
    database.save_top_long_short_position_ratio(bars)


if __name__ == "__main__":
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
    # symbol = "ETHUSDT"
    # symbol = "ETHBTC"
    # symbol = "ethusdt"  # spot for lower case while the future will be upper case.

    exchange = Exchange.BINANCE  # binance.

    fetch_data(gate_way, database, "ETHUSDT", exchange, Interval.MINUTE_15, datetime(2025, 12, 28))
    fetch_data(gate_way, database, "BTCUSDT", exchange, Interval.MINUTE_15, datetime(2025, 12, 28))
    fetch_data(gate_way, database, "ETHUSDT", exchange, Interval.MINUTE_5, datetime(2025, 12, 28))
    fetch_data(gate_way, database, "BTCUSDT", exchange, Interval.MINUTE_5, datetime(2025, 12, 28))

    print('success')
