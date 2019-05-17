import sqlalchemy

metadata = sqlalchemy.MetaData()

live_assets = sqlalchemy.Table(
    'liveasset', metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('code', sqlalchemy.String()),
    sqlalchemy.Column('is_live', sqlalchemy.Boolean),
)

trading_prices = sqlalchemy.Table(
    'tradingprice', metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('asset', sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column('ts', sqlalchemy.DateTime(), nullable=False),
    sqlalchemy.Column('price', sqlalchemy.Float(), nullable=False),
    sqlalchemy.Column('volume_cum', sqlalchemy.Float(), nullable=False),
    sqlalchemy.Column('bid', sqlalchemy.Float()),
    sqlalchemy.Column('bid', sqlalchemy.Float()),
    sqlalchemy.Column('bid_size', sqlalchemy.Float()),
    sqlalchemy.Column('ask', sqlalchemy.Float()),
    sqlalchemy.Column('ask_size', sqlalchemy.Float()),
)