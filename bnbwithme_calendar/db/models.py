from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, DateTime, PickleType, Enum, LargeBinary, BigInteger, TIMESTAMP, VARCHAR, Date, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum
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
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    name = Column(VARCHAR)
    color = Column(VARCHAR)
    owner_id = Column(BigInteger)
    icals = relationship("Ical", backref="location")
    reservations = relationship("Reservation", backref="location")

class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(BigInteger, primary_key=True)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    start = Column(Date)
    end = Column(Date)
    cleaner_id = Column(BigInteger)
    property_id = Column(BigInteger, ForeignKey('properties.id'))
    ical_id = Column(BigInteger)
    duration = Column(Integer)

class Ical(Base):
    __tablename__ = "icals"
    id = Column(BigInteger, primary_key=True)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    service = Column(Integer)
    link = Column(Text)
    property_id = Column(BigInteger, ForeignKey('properties.id'))

    def site(self):
        return service_map[self.service]

def connect():
    conf = config.get()
    c = conf["postgresql"]
    return create_engine(f'postgresql://{c["user"]}:{c["pass"]}@{c["host"]}:{c["port"]}/{c["db"]}')