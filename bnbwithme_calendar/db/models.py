from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, DateTime, BigInteger, Date, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
import enum, datetime
from . import config
Base = declarative_base()

class Service(enum.Enum):
  airbnb = 0
  vrbo = 1

service_map = {
  0 : Service.airbnb,
  1 : Service.vrbo
}

class Property(Base):
  __tablename__ = "properties"
  id = Column(BigInteger, primary_key=True)
  created_at = Column(DateTime)
  updated_at = Column(DateTime)
  name = Column(String)
  color = Column(String)
  owner_id = Column(BigInteger)
  icals = relationship("Ical", backref="location")
  reservations = relationship("Reservation", backref="location")

class Reservation(Base):
  __tablename__ = "reservations"
  id = Column(BigInteger, primary_key=True)
  created_at = Column(DateTime, default=datetime.datetime.utcnow)
  updated_at = Column(DateTime, default=datetime.datetime.utcnow)
  start = Column(Date)
  end = Column(Date)
  guest = Column(String)
  phone = Column(String)
  email = Column(String)
  cleaner_id = Column(BigInteger)
  property_id = Column(BigInteger, ForeignKey('properties.id'))
  ical_id = Column(BigInteger, ForeignKey('icals.id'))
  duration = Column(Integer)

class Ical(Base):
  __tablename__ = "icals"
  id = Column(BigInteger, primary_key=True)
  created_at = Column(DateTime)
  updated_at = Column(DateTime)
  service = Column(Integer)
  link = Column(Text)
  property_id = Column(BigInteger, ForeignKey('properties.id'))
  reservations = relationship("Reservation", backref="ical")

  def site(self):
    return service_map[self.service]

def connect():
  conf = config.get()
  c = conf["postgresql"]
  return create_engine(f'postgresql://{c["user"]}:{c["pass"]}@{c["host"]}:{c["port"]}/{c["db"]}')

def session():
  e = connect()
  session_factory = sessionmaker(bind=e)
  return scoped_session(session_factory)