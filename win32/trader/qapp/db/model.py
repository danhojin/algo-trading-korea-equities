from datetime import date
from pony.orm import (
    Database,
    PrimaryKey,
    Required,
    Optional,
    Set,
)


db = Database(
    provider='sqlite',
    filename='portfolio.sqlite3',
    # filename='portfolio_test.sqlite3',
    create_db=True
)


class Asset(db.Entity):
    id = PrimaryKey(int, auto=True)
    symbol = Required(str)
    num_shares = Required(int, default=0)  # number of shares
    max_shares = Required(int, default=50)
    position_size = Required(int, default=1)  # position size
    entries = Set('Entry')
    is_active = Required(bool, default=False)
    tactic = Optional('Tactic')


class Entry(db.Entity):
    id = PrimaryKey(int, auto=True)
    asset = Required(Asset)
    date = Required(date)
    price = Required(float)
    order = Required(int)  # completed transaction


class Tactic(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    endpoint = Required(str)
    assets = Set(Asset)


db.generate_mapping(create_tables=True)