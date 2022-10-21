import datetime
import enum

from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import relationship

from .base import db

today = datetime.datetime.now()
offer_ended = today + relativedelta(minutes=15)


class OfferType(enum.Enum):
    buy = 'Buy'
    sell = 'Sell'


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    tg_id = db.Column(db.BigInteger, unique=True)
    name = db.Column(db.String(32))
    offers = relationship("Offer")

    # Some methods here


class Offer(db.Model):
    __tablename__ = 'offers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    key_price = db.Column(db.Float)
    count_keys = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=today)
    ended_ad = db.Column(db.DateTime, default=offer_ended)
    offer_type = db.Column(db.Enum(OfferType))
    trx_hash = db.Column(db.String(255), unique=True)


class Keys(db.Model):
    __tablename__ = 'keys'

    id = db.Column(db.Integer, primary_key=True)
    user_buy_price = db.Column(db.Float, default=1.73)
    user_sell_price = db.Column(db.Float, default=1.66)
    user_max_buy = db.Column(db.Integer, default=1500)
    user_max_sell = db.Column(db.Integer, default=10)
