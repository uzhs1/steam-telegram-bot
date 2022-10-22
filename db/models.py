import datetime
import enum

from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM

from .base import db

today = datetime.datetime.now()
offer_ended = today + relativedelta(minutes=15)


@enum.unique
class OfferTypeEnum(enum.Enum):
    buy = 'Buy'
    sell = 'Sell'


@enum.unique
class OfferStatusEnum(enum.Enum):
    created_status = 'Created'
    ended_status = 'Ended'


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    tg_id = db.Column(db.BigInteger, unique=True)
    name = db.Column(db.String(32))
    offers = relationship('Offer')
    transactions = relationship('Transaction')

    # Some methods here


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    trx_hash = db.Column(db.String(150), unique=True)
    amount = db.Column(db.Float)
    offers = relationship('Offer')


class Offer(db.Model):
    __tablename__ = 'offers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    key_price = db.Column(db.Float)
    count_keys = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=today)
    ended_ad = db.Column(db.DateTime, default=offer_ended)
    offer_type = db.Column(ENUM(OfferTypeEnum))
    offer_status = db.Column(ENUM(OfferStatusEnum))
    trx_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), nullable=True)


class Keys(db.Model):
    __tablename__ = 'keys'

    id = db.Column(db.Integer, primary_key=True)
    user_buy_price = db.Column(db.Float, default=1.73)
    user_sell_price = db.Column(db.Float, default=1.66)
    user_max_buy = db.Column(db.Integer, default=1500)
    user_max_sell = db.Column(db.Integer, default=10)


