#!/usr/bin/python3
from db import models
from helpers.icalendar.services import reduce_connection
import datetime, time, logging
Session = models.session()

logging.basicConfig(filename='bnbwithme-calendar.log', level=logging.INFO)
s = Session()

def log_change(prepend:str, ical, reservation):
  return f'{prepend}: (property - {ical.location.name}) (start - {reservation.start}) (end {reservation.end}) (guest - {reservation.guest}) (service {ical.service})'

# Only sync 3 at a time.
icals = s.query(models.Ical).order_by(models.Ical.updated_at).limit(3)
for ical in icals:
  ical_connection = reduce_connection(ical)

  if not ical_connection.alive:
    logging.error(f'ICAL Failed to Download or Parse: {ical.id} {ical.link} {ical.location.name}')
    continue

  date_map = dict()
  # Check for reservations
  for reservation in ical_connection.reservations:
    date_map[reservation.start] = reservation.end
    search = s.query(models.Reservation).filter_by(ical=ical).filter_by(start=reservation.start).filter_by(end=reservation.end)
    # New listing detected, add ical and add to location
    if search.first() is None:
      reservation.ical = ical
      ical.location.reservations.append(reservation)
      logging.info(log_change("ADDING", ical, reservation))
  # Reverse check reservations
  search = s.query(models.Reservation).filter_by(ical=ical).filter(models.Reservation.end >= datetime.datetime.now().date()).all()
  if len(ical_connection.reservations) == 0:
    print(search)
    logging.warning(f'ICAL Feed Empty: {ical.id} {ical.link} {ical.location.name}')
  for reservation in search:
    end_date = date_map.get(reservation.start)
    match = False
    if end_date:
      match = reservation.end == end_date
    if not match:
      # Can only get to this point if there was no matching reservation in ical feed
      logging.warning(log_change("DELETING", ical, reservation))
      s.query(models.Reservation).filter_by(id=reservation.id).delete()
  ical.updated_at = datetime.datetime.utcnow()
  s.commit()
  print(ical.updated_at)
