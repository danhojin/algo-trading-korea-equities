# coding: utf-8
# with help of sqlacodegen: https://github.com/agronholm/sqlacodegen
# https://python-gino.readthedocs.io/en/latest/tutorial.html
from gino import Gino

db = Gino()


class Asset(db.Model):
    __tablename__ = 'asset'

    code = db.Column(db.Text(), primary_key=True)
    name = db.Column(db.Text(), nullable=False)
    is_active = db.Column(db.Boolean())
    is_adjusted = db.Column(db.Boolean())


class Dailyprice(db.Model):
    __tablename__ = 'dailyprice'

    id = db.Column(db.Integer(), primary_key=True,
                   server_default=db.text(
                       "nextval('dailyprice_id_seq'::regclass)"))
    date = db.Column(db.Date(), nullable=False)
    open = db.Column(db.Float())
    high = db.Column(db.Float())
    low = db.Column(db.Float())
    close = db.Column(db.Float(), nullable=False)
    volume = db.Column(db.Float(), nullable=False)
    asset = db.Column(db.ForeignKey('asset.code', ondelete='CASCADE'),
                      nullable=False, index=True)


class Marketindex(db.Model):
    __tablename__ = 'marketindex'

    id = db.Column(db.Integer(), primary_key=True,
                   server_default=db.text(
                       "nextval('marketindex_id_seq'::regclass)"))
    name = db.Column(db.Text(), nullable=False)
    asset = db.Column(db.ForeignKey('asset.code', ondelete='CASCADE'),
                      nullable=False, index=True)
