from datetime import date
from pony.orm import (
    Database,
    PrimaryKey,
    Set,
    Optional,
    Required,
)

db = Database()


class Asset(db.Entity):
    code = PrimaryKey(str, auto=True)
    market_indices = Set('MarketIndex')
    name = Optional(str)
    is_active = Optional(bool)
    daily_prices = Set('DailyPrice')
    is_adjusted = Optional(bool, default=False)


class DailyPrice(db.Entity):
    id = PrimaryKey(int, auto=True)
    date = Required(date)
    open = Optional(float)
    high = Optional(float)
    low = Optional(float)
    close = Required(float)
    volume = Required(float)
    asset = Required(Asset)


class MarketIndex(db.Entity):
    id = PrimaryKey(int, auto=True)
    asset = Required(Asset)
    name = Required(str)
