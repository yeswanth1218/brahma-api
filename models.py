# models.py
from sqlalchemy import Column, Integer, Text, Boolean, DateTime
from database import Base
from datetime import datetime
import pytz

class UserInput(Base):
    __tablename__ = "user_input"

    id = Column(Integer, primary_key=True, index=True)
    refined_user_input = Column(Text, nullable=False)
    time_and_date = Column(DateTime, nullable=False)
    consider = Column(Boolean, default=True)