from sqlalchemy import Column, BLOB
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class State(Base):
    __tablename__ = "amitystate"
    amity_state = Column(BLOB, primary_key=True)




