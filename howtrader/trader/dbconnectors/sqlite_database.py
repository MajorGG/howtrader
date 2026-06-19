from datetime import datetime
from typing import List

from peewee import (
    AutoField,
    CharField,
    DateTimeField,
    FloatField, IntegerField,
    Model,
    SqliteDatabase as PeeweeSqliteDatabase,
    ModelSelect,
    ModelDelete,
    chunked,
    fn
)

from howtrader.trader.constant import Exchange, Interval, Direction
from howtrader.trader.object import BarData, TickData, OpenInterestHist, TopLongShortAccountRatio, TopLongShortPositionRatio, GlobalLongShortAccountRatio, TakerLongShortRatio, TradeRecordData
from howtrader.trader.utility import get_file_path
from howtrader.trader.database import (
    BaseDatabase,
    BarOverview,
    DB_TZ,
    convert_tz
)


path = str(get_file_path("database.db"))
db = PeeweeSqliteDatabase(path)


class DbBarData(Model):
    """BarData model"""

    id = AutoField()

    symbol: str = CharField()
    exchange: str = CharField()
    datetime: DateTimeField = DateTimeField()
    interval: str = CharField()

    volume: float = FloatField()
    turnover: float = FloatField()
    open_interest: float = FloatField()
    open_price: float = FloatField()
    high_price: float = FloatField()
    low_price: float = FloatField()
    close_price: float = FloatField()
    cnt: int = IntegerField()
    buy_vol: float = FloatField()
    buy_amt: float = FloatField()

    class Meta:
        database = db
        indexes = ((("symbol", "exchange", "interval", "datetime"), True),)


class DbOpenInterestHist(Model):
    """BarData model"""

    id = AutoField()

    symbol: str = CharField()
    exchange: str = CharField()
    datetime: DateTimeField = DateTimeField()
    interval: str = CharField()

    sumOpenInterest: float = FloatField()
    sumOpenInterestValue: float = FloatField()
    CMCCirculatingSupply: float = FloatField()

    class Meta:
        database = db
        indexes = ((("symbol", "exchange", "interval", "datetime"), True),)


class DbTopLongShortPositionRatio(Model):
    """BarData model"""

    id = AutoField()

    symbol: str = CharField()
    exchange: str = CharField()
    datetime: DateTimeField = DateTimeField()
    interval: str = CharField()

    longShortRatio: float = FloatField()
    longAccount: float = FloatField()
    shortAccount: float = FloatField()

    class Meta:
        database = db
        indexes = ((("symbol", "exchange", "interval", "datetime"), True),)


class DbTopLongShortAccountRatio(Model):
    """BarData model"""

    id = AutoField()

    symbol: str = CharField()
    exchange: str = CharField()
    datetime: DateTimeField = DateTimeField()
    interval: str = CharField()

    longShortRatio: float = FloatField()
    longAccount: float = FloatField()
    shortAccount: float = FloatField()

    class Meta:
        database = db
        indexes = ((("symbol", "exchange", "interval", "datetime"), True),)


class DbGlobalLongShortAccountRatio(Model):
    """BarData model"""

    id = AutoField()

    symbol: str = CharField()
    exchange: str = CharField()
    datetime: DateTimeField = DateTimeField()
    interval: str = CharField()

    longShortRatio: float = FloatField()
    longAccount: float = FloatField()
    shortAccount: float = FloatField()

    class Meta:
        database = db
        indexes = ((("symbol", "exchange", "interval", "datetime"), True),)


class DbTakerLongShortRatio(Model):
    """BarData model"""

    id = AutoField()

    symbol: str = CharField()
    exchange: str = CharField()
    datetime: DateTimeField = DateTimeField()
    interval: str = CharField()

    buySellRatio: float = FloatField()
    buyVol: float = FloatField()
    sellVol: float = FloatField()

    class Meta:
        database = db
        indexes = ((("symbol", "exchange", "interval", "datetime"), True),)


class DbTradeRecord(Model):
    """BarData model"""

    id = AutoField()

    symbol: str = CharField()
    exchange: str = CharField()
    trade_type: str = CharField()
    order_id: str = CharField()
    trade_id: str = CharField()
    direction: str = CharField()

    price: float = FloatField()
    volume: float = FloatField()
    order_time: DateTimeField = DateTimeField()
    trade_time: DateTimeField = DateTimeField()

    class Meta:
        database = db
        indexes = ((("symbol", "exchange", "trade_type", "trade_time"), True),)


class DbTickData(Model):
    """Tick Data Model"""

    id = AutoField()

    symbol: str = CharField()
    exchange: str = CharField()
    datetime: datetime = DateTimeField()

    name: str = CharField()
    volume: float = FloatField()
    turnover: float = FloatField()
    open_interest: float = FloatField()
    last_price: float = FloatField()
    last_volume: float = FloatField()
    limit_up: float = FloatField()
    limit_down: float = FloatField()

    open_price: float = FloatField()
    high_price: float = FloatField()
    low_price: float = FloatField()
    pre_close: float = FloatField()

    bid_price_1: float = FloatField()
    bid_price_2: float = FloatField(null=True)
    bid_price_3: float = FloatField(null=True)
    bid_price_4: float = FloatField(null=True)
    bid_price_5: float = FloatField(null=True)

    ask_price_1: float = FloatField()
    ask_price_2: float = FloatField(null=True)
    ask_price_3: float = FloatField(null=True)
    ask_price_4: float = FloatField(null=True)
    ask_price_5: float = FloatField(null=True)

    bid_volume_1: float = FloatField()
    bid_volume_2: float = FloatField(null=True)
    bid_volume_3: float = FloatField(null=True)
    bid_volume_4: float = FloatField(null=True)
    bid_volume_5: float = FloatField(null=True)

    ask_volume_1: float = FloatField()
    ask_volume_2: float = FloatField(null=True)
    ask_volume_3: float = FloatField(null=True)
    ask_volume_4: float = FloatField(null=True)
    ask_volume_5: float = FloatField(null=True)

    localtime: datetime = DateTimeField(null=True)

    class Meta:
        database = db
        indexes = ((("symbol", "exchange", "datetime"), True),)


class DbBarOverview(Model):
    """DbBar Overview Model"""

    id = AutoField()

    symbol: str = CharField()
    exchange: str = CharField()
    interval: str = CharField()
    count: int = IntegerField()
    start: datetime = DateTimeField()
    end: datetime = DateTimeField()

    class Meta:
        database = db
        indexes = ((("symbol", "exchange", "interval"), True),)


class SqliteDatabase(BaseDatabase):
    """sqlite Database connector"""

    def __init__(self) -> None:
        """"""
        self.db = db
        self.db.connect()
        self.db.create_tables([DbBarData, DbTickData, DbBarOverview, DbTakerLongShortRatio,
                               DbTopLongShortAccountRatio, DbTopLongShortPositionRatio,
                               DbGlobalLongShortAccountRatio, DbOpenInterestHist, DbTradeRecord])

    def save_bar_data(self, bars: List[BarData]) -> bool:
        """save bar data"""
        # primary key
        bar = bars[0]
        symbol = bar.symbol
        exchange = bar.exchange
        interval = bar.interval

        # convert BarData into dict, and convert timezone
        data = []

        for bar in bars:
            bar.datetime = convert_tz(bar.datetime)

            d = bar.__dict__
            d["exchange"] = d["exchange"].value
            d["interval"] = d["interval"].value
            d.pop("gateway_name")
            d.pop("vt_symbol")
            data.append(d)

        # use upsert to update data into database
        with self.db.atomic():
            for c in chunked(data, 50):
                DbBarData.insert_many(c).on_conflict_replace().execute()

        # update DbBarOverview data
        overview: DbBarOverview = DbBarOverview.get_or_none(
            DbBarOverview.symbol == symbol,
            DbBarOverview.exchange == exchange.value,
            DbBarOverview.interval == interval.value,
        )

        if not overview:
            overview = DbBarOverview()
            overview.symbol = symbol
            overview.exchange = exchange.value
            overview.interval = interval.value
            overview.start = bars[0].datetime
            overview.end = bars[-1].datetime
            overview.count = len(bars)
        else:
            overview.start = min(bars[0].datetime, overview.start)
            overview.end = max(bars[-1].datetime, overview.end)

            s: ModelSelect = DbBarData.select().where(
                (DbBarData.symbol == symbol)
                & (DbBarData.exchange == exchange.value)
                & (DbBarData.interval == interval.value)
            )
            overview.count = s.count()

        overview.save()

        return True

    def save_open_interest_hist(self, bars: List[OpenInterestHist]) -> bool:

        data = []

        for bar in bars:
            bar.datetime = convert_tz(bar.datetime)

            d = bar.__dict__
            d["exchange"] = d["exchange"].value
            d["interval"] = d["interval"].value
            d.pop("gateway_name")
            d.pop("vt_symbol")
            data.append(d)

        # use upsert to update data into database
        with self.db.atomic():
            for c in chunked(data, 50):
                DbOpenInterestHist.insert_many(c).on_conflict_replace().execute()

        return True

    def save_global_long_short_account_ratio(self, bars: List[GlobalLongShortAccountRatio]) -> bool:

        data = []

        for bar in bars:
            bar.datetime = convert_tz(bar.datetime)

            d = bar.__dict__
            d["exchange"] = d["exchange"].value
            d["interval"] = d["interval"].value
            d.pop("gateway_name")
            d.pop("vt_symbol")
            data.append(d)

        # use upsert to update data into database
        with self.db.atomic():
            for c in chunked(data, 50):
                DbGlobalLongShortAccountRatio.insert_many(c).on_conflict_replace().execute()

        return True

    def save_taker_long_short_ratio(self, bars: List[TakerLongShortRatio]) -> bool:

        data = []

        for bar in bars:
            bar.datetime = convert_tz(bar.datetime)

            d = bar.__dict__
            d["exchange"] = d["exchange"].value
            d["interval"] = d["interval"].value
            d.pop("gateway_name")
            d.pop("vt_symbol")
            data.append(d)

        # use upsert to update data into database
        with self.db.atomic():
            for c in chunked(data, 50):
                DbTakerLongShortRatio.insert_many(c).on_conflict_replace().execute()

        return True

    def save_top_long_short_account_ratio(self, bars: List[TopLongShortAccountRatio]) -> bool:

        data = []

        for bar in bars:
            bar.datetime = convert_tz(bar.datetime)

            d = bar.__dict__
            d["exchange"] = d["exchange"].value
            d["interval"] = d["interval"].value
            d.pop("gateway_name")
            d.pop("vt_symbol")
            data.append(d)

        # use upsert to update data into database
        with self.db.atomic():
            for c in chunked(data, 50):
                DbTopLongShortAccountRatio.insert_many(c).on_conflict_replace().execute()

        return True

    def save_top_long_short_position_ratio(self, bars: List[TopLongShortPositionRatio]) -> bool:

        data = []

        for bar in bars:
            bar.datetime = convert_tz(bar.datetime)

            d = bar.__dict__
            d["exchange"] = d["exchange"].value
            d["interval"] = d["interval"].value
            d.pop("gateway_name")
            d.pop("vt_symbol")
            data.append(d)

        # use upsert to update data into database
        with self.db.atomic():
            for c in chunked(data, 50):
                DbTopLongShortPositionRatio.insert_many(c).on_conflict_replace().execute()

        return True

    def save_tick_data(self, ticks: List[TickData]) -> bool:
        """save tick data"""
        # convert tickdata into dict, and convert its timezone
        data = []

        for tick in ticks:
            tick.datetime = convert_tz(tick.datetime)

            d = tick.__dict__
            d["exchange"] = d["exchange"].value
            d.pop("gateway_name")
            d.pop("vt_symbol")
            data.append(d)

        # use update to update data into database
        with self.db.atomic():
            for c in chunked(data, 10):
                DbTickData.insert_many(c).on_conflict_replace().execute()

        return True

    def save_trade_record_data(self, records: List[TradeRecordData]) -> bool:
        data = []

        for record in records:
            record.order_time = convert_tz(record.order_time)
            record.trade_time = convert_tz(record.trade_time)

            d = record.__dict__
            d["exchange"] = d["exchange"].value
            d["direction"] = d["direction"].value
            d.pop("gateway_name")
            d.pop("vt_symbol")
            data.append(d)

        # use update to update data into database
        with self.db.atomic():
            for c in chunked(data, 10):
                DbTradeRecord.insert_many(c).on_conflict_replace().execute()

        return True

    def load_trade_record(
        self,
        symbol: str,
        exchange: Exchange,
        trade_type: str,
        limit: int = 100,
        start: datetime = None
    ) -> List[TradeRecordData]:
        s: ModelSelect = (
            DbTradeRecord.select().where(
                (DbTradeRecord.symbol == symbol)
                & (DbTradeRecord.exchange == exchange.value)
                & (DbTradeRecord.trade_type == trade_type)
            )
        )

        if start:
            s.where(DbTradeRecord.trade_time >= start)

        s.order_by(DbTradeRecord.trade_time)
        s.limit(limit)

        records: List[TradeRecordData] = []
        for db_bar in s:
            bar = TradeRecordData(
                symbol=db_bar.symbol,
                exchange=Exchange(db_bar.exchange),
                trade_type=db_bar.trade_type,
                order_id=db_bar.order_id,
                trade_id=db_bar.trade_id,
                direction=Direction(db_bar.direction),
                price=db_bar.price,
                volume=db_bar.volume,
                order_time=datetime.fromtimestamp(db_bar.order_time.timestamp(), DB_TZ),
                trade_time=datetime.fromtimestamp(db_bar.trade_time.timestamp(), DB_TZ),
                gateway_name="DB"
            )
            records.append(bar)

        return records

    def load_open_interest_hist(
        self,
        symbol: str,
        exchange: Exchange,
        interval: Interval,
        start: datetime,
        end: datetime
    ) -> List[OpenInterestHist]:
        s: ModelSelect = (
            DbOpenInterestHist.select().where(
                (DbOpenInterestHist.symbol == symbol)
                & (DbOpenInterestHist.exchange == exchange.value)
                & (DbOpenInterestHist.interval == interval.value)
                & (DbOpenInterestHist.datetime >= start)
                & (DbOpenInterestHist.datetime <= end)
            ).order_by(DbOpenInterestHist.datetime)
        )

        bars: List[OpenInterestHist] = []
        for db_bar in s:
            bar = OpenInterestHist(
                symbol=db_bar.symbol,
                exchange=Exchange(db_bar.exchange),
                datetime=datetime.fromtimestamp(db_bar.datetime.timestamp(), DB_TZ),
                interval=Interval(db_bar.interval),
                sumOpenInterest=db_bar.sumOpenInterest,
                sumOpenInterestValue=db_bar.sumOpenInterestValue,
                CMCCirculatingSupply=db_bar.CMCCirculatingSupply,
                gateway_name="DB"
            )
            bars.append(bar)

        return bars

    def load_global_long_short_account_ratio(
        self,
        symbol: str,
        exchange: Exchange,
        interval: Interval,
        start: datetime,
        end: datetime
    ) -> List[GlobalLongShortAccountRatio]:
        s: ModelSelect = (
            DbGlobalLongShortAccountRatio.select().where(
                (DbGlobalLongShortAccountRatio.symbol == symbol)
                & (DbGlobalLongShortAccountRatio.exchange == exchange.value)
                & (DbGlobalLongShortAccountRatio.interval == interval.value)
                & (DbGlobalLongShortAccountRatio.datetime >= start)
                & (DbGlobalLongShortAccountRatio.datetime <= end)
            ).order_by(DbGlobalLongShortAccountRatio.datetime)
        )

        bars: List[GlobalLongShortAccountRatio] = []
        for db_bar in s:
            bar = GlobalLongShortAccountRatio(
                symbol=db_bar.symbol,
                exchange=Exchange(db_bar.exchange),
                datetime=datetime.fromtimestamp(db_bar.datetime.timestamp(), DB_TZ),
                interval=Interval(db_bar.interval),
                longShortRatio=db_bar.longShortRatio,
                longAccount=db_bar.longAccount,
                shortAccount=db_bar.shortAccount,
                gateway_name="DB"
            )
            bars.append(bar)

        return bars

    def load_taker_long_short_ratio(
        self,
        symbol: str,
        exchange: Exchange,
        interval: Interval,
        start: datetime,
        end: datetime
    ) -> List[TakerLongShortRatio]:
        s: ModelSelect = (
            DbTakerLongShortRatio.select().where(
                (DbTakerLongShortRatio.symbol == symbol)
                & (DbTakerLongShortRatio.exchange == exchange.value)
                & (DbTakerLongShortRatio.interval == interval.value)
                & (DbTakerLongShortRatio.datetime >= start)
                & (DbTakerLongShortRatio.datetime <= end)
            ).order_by(DbTakerLongShortRatio.datetime)
        )

        bars: List[TakerLongShortRatio] = []
        for db_bar in s:
            bar = TakerLongShortRatio(
                symbol=db_bar.symbol,
                exchange=Exchange(db_bar.exchange),
                datetime=datetime.fromtimestamp(db_bar.datetime.timestamp(), DB_TZ),
                interval=Interval(db_bar.interval),
                buySellRatio=db_bar.buySellRatio,
                buyVol=db_bar.buyVol,
                sellVol=db_bar.sellVol,
                gateway_name="DB"
            )
            bars.append(bar)

        return bars

    def load_top_long_short_account_ratio(
        self,
        symbol: str,
        exchange: Exchange,
        interval: Interval,
        start: datetime,
        end: datetime
    ) -> List[TopLongShortAccountRatio]:
        s: ModelSelect = (
            DbTopLongShortAccountRatio.select().where(
                (DbTopLongShortAccountRatio.symbol == symbol)
                & (DbTopLongShortAccountRatio.exchange == exchange.value)
                & (DbTopLongShortAccountRatio.interval == interval.value)
                & (DbTopLongShortAccountRatio.datetime >= start)
                & (DbTopLongShortAccountRatio.datetime <= end)
            ).order_by(DbTopLongShortAccountRatio.datetime)
        )
        bars: List[TopLongShortAccountRatio] = []
        for db_bar in s:
            bar = TopLongShortAccountRatio(
                symbol=db_bar.symbol,
                exchange=Exchange(db_bar.exchange),
                datetime=datetime.fromtimestamp(db_bar.datetime.timestamp(), DB_TZ),
                interval=Interval(db_bar.interval),
                longShortRatio=db_bar.longShortRatio,
                longAccount=db_bar.longAccount,
                shortAccount=db_bar.shortAccount,
                gateway_name="DB"
            )
            bars.append(bar)

        return bars

    def load_top_long_short_position_ratio(
        self,
        symbol: str,
        exchange: Exchange,
        interval: Interval,
        start: datetime,
        end: datetime
    ) -> List[TopLongShortPositionRatio]:
        s: ModelSelect = (
            DbTopLongShortPositionRatio.select().where(
                (DbTopLongShortPositionRatio.symbol == symbol)
                & (DbTopLongShortPositionRatio.exchange == exchange.value)
                & (DbTopLongShortPositionRatio.interval == interval.value)
                & (DbTopLongShortPositionRatio.datetime >= start)
                & (DbTopLongShortPositionRatio.datetime <= end)
            ).order_by(DbTopLongShortPositionRatio.datetime)
        )
        bars: List[TopLongShortPositionRatio] = []
        for db_bar in s:
            bar = TopLongShortPositionRatio(
                symbol=db_bar.symbol,
                exchange=Exchange(db_bar.exchange),
                datetime=datetime.fromtimestamp(db_bar.datetime.timestamp(), DB_TZ),
                interval=Interval(db_bar.interval),
                longShortRatio=db_bar.longShortRatio,
                longAccount=db_bar.longAccount,
                shortAccount=db_bar.shortAccount,
                gateway_name="DB"
            )
            bars.append(bar)

        return bars

    def load_bar_data(
        self,
        symbol: str,
        exchange: Exchange,
        interval: Interval,
        start: datetime,
        end: datetime
    ) -> List[BarData]:
        """load bar data"""
        s: ModelSelect = (
            DbBarData.select().where(
                (DbBarData.symbol == symbol)
                & (DbBarData.exchange == exchange.value)
                & (DbBarData.interval == interval.value)
                & (DbBarData.datetime >= start)
                & (DbBarData.datetime <= end)
            ).order_by(DbBarData.datetime)
        )

        bars: List[BarData] = []
        for db_bar in s:
            bar = BarData(
                symbol=db_bar.symbol,
                exchange=Exchange(db_bar.exchange),
                datetime=datetime.fromtimestamp(db_bar.datetime.timestamp(), DB_TZ),
                interval=Interval(db_bar.interval),
                volume=db_bar.volume,
                turnover=db_bar.turnover,
                open_interest=db_bar.open_interest,
                open_price=db_bar.open_price,
                high_price=db_bar.high_price,
                low_price=db_bar.low_price,
                close_price=db_bar.close_price,
                cnt=db_bar.cnt,
                buy_vol=db_bar.buy_vol,
                buy_amt=db_bar.buy_amt,
                gateway_name="DB"
            )
            bars.append(bar)

        return bars

    def load_tick_data(
        self,
        symbol: str,
        exchange: Exchange,
        start: datetime,
        end: datetime
    ) -> List[TickData]:
        """load tick data"""
        s: ModelSelect = (
            DbTickData.select().where(
                (DbTickData.symbol == symbol)
                & (DbTickData.exchange == exchange.value)
                & (DbTickData.datetime >= start)
                & (DbTickData.datetime <= end)
            ).order_by(DbTickData.datetime)
        )

        ticks: List[TickData] = []
        for db_tick in s:
            tick = TickData(
                symbol=db_tick.symbol,
                exchange=Exchange(db_tick.exchange),
                datetime=datetime.fromtimestamp(db_tick.datetime.timestamp(), DB_TZ),
                name=db_tick.name,
                volume=db_tick.volume,
                turnover=db_tick.turnover,
                open_interest=db_tick.open_interest,
                last_price=db_tick.last_price,
                last_volume=db_tick.last_volume,
                limit_up=db_tick.limit_up,
                limit_down=db_tick.limit_down,
                open_price=db_tick.open_price,
                high_price=db_tick.high_price,
                low_price=db_tick.low_price,
                pre_close=db_tick.pre_close,
                bid_price_1=db_tick.bid_price_1,
                bid_price_2=db_tick.bid_price_2,
                bid_price_3=db_tick.bid_price_3,
                bid_price_4=db_tick.bid_price_4,
                bid_price_5=db_tick.bid_price_5,
                ask_price_1=db_tick.ask_price_1,
                ask_price_2=db_tick.ask_price_2,
                ask_price_3=db_tick.ask_price_3,
                ask_price_4=db_tick.ask_price_4,
                ask_price_5=db_tick.ask_price_5,
                bid_volume_1=db_tick.bid_volume_1,
                bid_volume_2=db_tick.bid_volume_2,
                bid_volume_3=db_tick.bid_volume_3,
                bid_volume_4=db_tick.bid_volume_4,
                bid_volume_5=db_tick.bid_volume_5,
                ask_volume_1=db_tick.ask_volume_1,
                ask_volume_2=db_tick.ask_volume_2,
                ask_volume_3=db_tick.ask_volume_3,
                ask_volume_4=db_tick.ask_volume_4,
                ask_volume_5=db_tick.ask_volume_5,
                localtime=db_tick.localtime,
                gateway_name="DB"
            )
            ticks.append(tick)

        return ticks

    def delete_bar_data(
        self,
        symbol: str,
        exchange: Exchange,
        interval: Interval
    ) -> int:
        """delete bar data"""
        d: ModelDelete = DbBarData.delete().where(
            (DbBarData.symbol == symbol)
            & (DbBarData.exchange == exchange.value)
            & (DbBarData.interval == interval.value)
        )
        count = d.execute()

        # delete DbBarData overview
        d2: ModelDelete = DbBarOverview.delete().where(
            (DbBarOverview.symbol == symbol)
            & (DbBarOverview.exchange == exchange.value)
            & (DbBarOverview.interval == interval.value)
        )
        d2.execute()

        return count

    def delete_tick_data(
        self,
        symbol: str,
        exchange: Exchange
    ) -> int:
        """delete tick data"""
        d: ModelDelete = DbTickData.delete().where(
            (DbTickData.symbol == symbol)
            & (DbTickData.exchange == exchange.value)
        )
        count = d.execute()
        return count

    def delete_open_interest_hist(
        self,
        symbol: str,
        exchange: Exchange
    ) -> int:
        """delete tick data"""
        d: ModelDelete = DbOpenInterestHist.delete().where(
            (DbOpenInterestHist.symbol == symbol)
            & (DbOpenInterestHist.exchange == exchange.value)
        )
        count = d.execute()
        return count

    def delete_global_long_short_account_ratio(
        self,
        symbol: str,
        exchange: Exchange
    ) -> int:
        """delete tick data"""
        d: ModelDelete = DbGlobalLongShortAccountRatio.delete().where(
            (DbGlobalLongShortAccountRatio.symbol == symbol)
            & (DbGlobalLongShortAccountRatio.exchange == exchange.value)
        )
        count = d.execute()
        return count

    def delete_taker_long_short_ratio(
        self,
        symbol: str,
        exchange: Exchange
    ) -> int:
        """delete tick data"""
        d: ModelDelete = DbTakerLongShortRatio.delete().where(
            (DbTakerLongShortRatio.symbol == symbol)
            & (DbTakerLongShortRatio.exchange == exchange.value)
        )
        count = d.execute()
        return count

    def delete_top_long_short_account_ratio(
        self,
        symbol: str,
        exchange: Exchange
    ) -> int:
        """delete tick data"""
        d: ModelDelete = DbTopLongShortAccountRatio.delete().where(
            (DbTopLongShortAccountRatio.symbol == symbol)
            & (DbTopLongShortAccountRatio.exchange == exchange.value)
        )
        count = d.execute()
        return count

    def delete_top_long_short_position_ratio(
        self,
        symbol: str,
        exchange: Exchange
    ) -> int:
        """delete tick data"""
        d: ModelDelete = DbTopLongShortPositionRatio.delete().where(
            (DbTopLongShortPositionRatio.symbol == symbol)
            & (DbTopLongShortPositionRatio.exchange == exchange.value)
        )
        count = d.execute()
        return count

    def get_bar_overview(self) -> List[BarOverview]:
        """query DbBarData overview"""
        # 如果已有K线，但缺失汇总信息，则执行初始化
        data_count = DbBarData.select().count()
        overview_count = DbBarOverview.select().count()
        if data_count and not overview_count:
            self.init_bar_overview()

        s: ModelSelect = DbBarOverview.select()
        overviews = []
        for overview in s:
            overview.exchange = Exchange(overview.exchange)
            overview.interval = Interval(overview.interval)
            overviews.append(overview)
        return overviews

    def init_bar_overview(self) -> None:
        """init DbBarData Overview"""
        s: ModelSelect = (
            DbBarData.select(
                DbBarData.symbol,
                DbBarData.exchange,
                DbBarData.interval,
                fn.COUNT(DbBarData.id).alias("count")
            ).group_by(
                DbBarData.symbol,
                DbBarData.exchange,
                DbBarData.interval
            )
        )

        for data in s:
            overview = DbBarOverview()
            overview.symbol = data.symbol
            overview.exchange = data.exchange
            overview.interval = data.interval
            overview.count = data.count

            start_bar: DbBarData = (
                DbBarData.select()
                .where(
                    (DbBarData.symbol == data.symbol)
                    & (DbBarData.exchange == data.exchange)
                    & (DbBarData.interval == data.interval)
                )
                .order_by(DbBarData.datetime.asc())
                .first()
            )
            overview.start = start_bar.datetime

            end_bar: DbBarData = (
                DbBarData.select()
                .where(
                    (DbBarData.symbol == data.symbol)
                    & (DbBarData.exchange == data.exchange)
                    & (DbBarData.interval == data.interval)
                )
                .order_by(DbBarData.datetime.desc())
                .first()
            )
            overview.end = end_bar.datetime

            overview.save()
