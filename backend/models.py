from database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime
import datetime

class Test(Base):
    __tablename__  = "test"
    id = Column(Integer,primary_key=True)
    name = Column(String)