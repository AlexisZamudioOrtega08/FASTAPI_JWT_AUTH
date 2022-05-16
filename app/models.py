from database import Base
from sqlalchemy import Column, String


class User(Base):
    __tablename__ = "users"
    id = Column(String(length=50), primary_key=True, index=True)
    username = Column(String(length=50), unique=True, index=True)
    password = Column(String(length=120), index=True)
