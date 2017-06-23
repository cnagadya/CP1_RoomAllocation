import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, BLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


# class Persons( Base ):
#     __tablename__ = 'persons'
#     id = Column( Integer, primary_key=True )
#     person_name = Column( String( 250 ), nullable=False )
#     person_type = Column( String( 250 ), nullable=False )
#     person_id = Column( Integer, nullable=False )
#
#     rooms = relationship( "Rooms", back_populates="peoples" )
#
#
# class Rooms( Base ):
#     __tablename__ = 'rooms'
#     id = Column( Integer, primary_key=True )
#     room_name = Column( String( 250 ), nullable=False )
#     room_type = Column( String( 250 ), nullable=False )
#     persons_id = Column( Integer, ForeignKey( 'persons.id' ) )
#     peoples = relationship( "Persons", back_populates="rooms" )


class State(Base):
    __tablename__ = "amitystate"
    amity_state = Column(BLOB, primary_key=True)




