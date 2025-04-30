from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Table, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
event_schema = {'schema': 'EventsDM'}


class Participant(Base):
    __tablename__ = 'EventParticipants'
    __table_args__ = event_schema
    
    UserId = Column(Integer, primary_key=True)
    FirstName = Column(String, nullable=False)
    LastName = Column(String, nullable=False)
    Dob = Column(DateTime, nullable=False)
    Email = Column(String, nullable=False)
    
    CreateDate = Column(DateTime, nullable=False)
    CreatedBy = Column(String, nullable=False)
    
    Events = relationship("Event", back_populates="Participant")
    ItemCollections = relationship("ItemCollection", back_populates="Participant")


class EventInfo(Base):
    __tablename__ = 'EventsInfo'
    __table_args__ = event_schema
    
    EventId = Column(Integer, primary_key=True, autoincrement=True)
    EventName = Column(String, nullable=False)
    EventLocation = Column(String, nullable=False)
    EventDate = Column(DateTime, nullable=False)
    
    CreateDate = Column(DateTime, nullable=False)
    CreatedBy = Column(String, nullable=False)
    
    Events = relationship("Event", back_populates="EventInfo")
    ItemCollections = relationship("ItemCollection", back_populates="EventInfo")


class Event(Base):
    __tablename__ = 'Events'
    __table_args__ = event_schema
    
    EventId = Column(Integer, ForeignKey('EventsDM.EventsInfo.EventId'), primary_key=True)
    UserId = Column(Integer, ForeignKey('EventsDM.EventParticipants.UserId'), primary_key=True)
    
    JoinDate = Column(DateTime, nullable=False)
    AddedBy = Column(String, nullable=True)
    
    CreateDate = Column(DateTime, nullable=False)
    CreatedBy = Column(String, nullable=False)
    
    Participant = relationship("Participant", back_populates="Events")
    EventInfo = relationship("EventInfo", back_populates="Events")


class EventItem(Base):
    __tablename__ = 'EventItems'
    __table_args__ = event_schema
    
    ItemId = Column(Integer, primary_key=True, autoincrement=True)
    ItemName = Column(String, nullable=False)
    ItemDescription = Column(String, nullable=True)
    IsGlobal = Column(Boolean, nullable=False, default=False)
    
    CreateDate = Column(DateTime, nullable=False)
    CreatedBy = Column(String, nullable=False)
    
    ItemCollections = relationship("ItemCollection", back_populates="EventItem")


class ItemCollection(Base):
    __tablename__ = 'ItemCollection'
    __table_args__ = event_schema
    
    UserId = Column(Integer, ForeignKey('EventsDM.EventParticipants.UserId'), primary_key=True)
    ItemId = Column(Integer, ForeignKey('EventsDM.EventItems.ItemId'), primary_key=True)
    EventId = Column(Integer, ForeignKey('EventsDM.EventsInfo.EventId'), primary_key=True)
    
    CreateDate = Column(DateTime, nullable=False)
    CreatedBy = Column(String, nullable=False)
    
    Participant = relationship("Participant", back_populates="ItemCollections")
    EventItem = relationship("EventItem", back_populates="ItemCollections")
    EventInfo = relationship("EventInfo", back_populates="ItemCollections")