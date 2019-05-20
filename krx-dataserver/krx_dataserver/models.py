# coding: utf-8
from sqlalchemy import (
    Boolean, Column, Date, Float, ForeignKey,
    Integer, MetaData, Table, Text, text
)

metadata = MetaData()

asset = Table(
    'asset', metadata,
    Column('code', Text, primary_key=True),
    Column('name', Text, nullable=False),
    Column('is_active', Boolean),
    Column('is_adjusted', Boolean)
)

dailyprice = Table(
    'dailyprice', metadata,
    Column('id', Integer, primary_key=True,
           server_default=text("nextval('dailyprice_id_seq'::regclass)")),
    Column('date', Date, nullable=False),
    Column('open', Float),
    Column('high', Float),
    Column('low', Float),
    Column('close', Float, nullable=False),
    Column('volume', Float, nullable=False),
    Column('asset', ForeignKey('asset.code', ondelete='CASCADE'),
           nullable=False, index=True)
)

marketindex = Table(
    'marketindex', metadata,
    Column('id', Integer, primary_key=True,
           server_default=text("nextval('marketindex_id_seq'::regclass)")),
    Column('name', Text, nullable=False),
    Column('asset', ForeignKey('asset.code', ondelete='CASCADE'),
           nullable=False, index=True)
)
