from pony.orm import (
    Database,
    PrimaryKey,
    Optional,
    Required,
    Set,
)
from .settings import (
    PG_USERNAME,
    PG_PASSWORD,
    PG_HOST,
    PG_DATABASE,
)
from datetime import date


db = Database(
    provider='postgres',
    user=PG_USERNAME,
    password=PG_PASSWORD,
    host=PG_HOST,
    database=PG_DATABASE,
)


class Asset(db.Entity):
    code = PrimaryKey(str, auto=True)
    name = Optional(str)
    is_active = Optional(str)
    daily_prices = Set('DailyPrice')
    is_adjusted = Optional(bool, default=False)
    market_indices = Set('MarketIndex')


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


db.generate_mapping(create_tables=True)
