from pony import orm

db = orm.Database(
    'sqlite',
    'db.sqlite3',
    create_db=True
)

class Asset(db.Entity):
    code = orm.PrimaryKey(str, auto=True)
    name = orm.Optional(str)
    market_indices = orm.Set('MarketIndex')


class MarketIndex(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    symbol = orm.Required(str)
    asset = orm.Required(Asset)

# turn on debug mode
# orm.sql_debug(True)

db.generate_mapping(create_tables=True)

@orm.db_session
def insert_into_Asset(assets):
    for asset in assets:
        a = Asset.get(code=asset['code'])
        if a is None:
            Asset(**asset)

@orm.db_session
def insert_into_MarketIndex(market_indices):
    for index in market_indices:
        i = MarketIndex.get(symbol=index['symbol'], asset=index['asset'])
        if i is None:
            MarketIndex(**index)