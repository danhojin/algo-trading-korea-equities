from pony import orm

db = orm.Database(
    'sqlite',
    'db.sqlite3',
    create_db=True
)

class Stock(db.Entity):
    code = orm.PrimaryKey(str, auto=True)
    name = orm.Optional(str)
    market_indices = orm.Set('MarketIndex')


class MarketIndex(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    symbol = orm.Required(str)
    stock = orm.Required(Stock)

# turn on debug mode
# orm.sql_debug(True)

db.generate_mapping(create_tables=True)

@orm.db_session
def insert_into_Stock(stocks):
    for stock in stocks:
        s = Stock.get(code=stock['code'])
        if s is None:
            Stock(**stock)

@orm.db_session
def insert_into_MarketIndex(market_indices):
    for index in market_indices:
        i = MarketIndex.get(symbol=index['symbol'], stock=index['stock'])
        if i is None:
            MarketIndex(**index)