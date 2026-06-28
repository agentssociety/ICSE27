from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class CardORM(Base):
    __tablename__ = "card"

    id = Column(Integer, primary_key=True)
    # Additional skeleton columns can be added below.