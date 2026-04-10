from database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey,func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship


class Test(Base):
    __tablename__  = "test"
    id = Column(Integer,primary_key=True)
    name = Column(String)

class Items(Base):
    __tablename__ = "items"
    id = Column(Integer,primary_key=True)
    name = Column(String(100),unique=True)
    image_url = Column(String(400))

class Markets(Base):
    __tablename__ = "markets"
    id = Column(Integer,primary_key=True)
    name = Column(String(50))
    fee = Column(Float)

class Prices(Base):
    __tablename__ = "prices"
    id = Column(Integer,primary_key=True)
    item_id = Column(Integer,ForeignKey('items.id'))
    market_id = Column(Integer,ForeignKey('markets.id'))
    price = Column(Float)
    update_date = Column(DateTime, default=func.now(), onupdate=func.now())

    market = relationship("Markets")

    @hybrid_property
    def price_after_fee(self):
        return self.price * (1-self.market.fee)

class ExchangeRate(Base):
    __tablename__ = "currency"
    id = Column(Integer, primary_key=True)
    name = Column(String(20),unique=True)
    rate = Column(Float)
