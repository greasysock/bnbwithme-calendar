#!/usr/bin/python3
from db import models
from helpers.icalendar import pull as ical_pull
import datetime, time, logging
Session = models.session()

logging.basicConfig(filename='bnbwithme-calendar.log',level=logging.INFO)
s = Session()

def log_change(prepend:str, ical, reservation):
        return f'{prepend}: (property - {ical.location.name}) (start - {reservation.start}) (end {reservation.end}) (guest - {reservation.guest}) (service {ical.service})'


# Only sync 3 at a time.
icals = s.query(models.Ical).order_by(models.Ical.updated_at).limit(3)
for ical in icals:       
    reservations = ical_pull.get_all_reservations(ical)
    date_map = dict()
    # Check for reservations
    for reservation in reservations:
        date_map[reservation.start] = reservation.end
        search = s.query(models.Reservation).filter_by(ical=ical).filter_by(start=reservation.start).filter_by(end=reservation.end)
        # New listing detected, add ical and add to location
        if search.first() is None:
            reservation.ical = ical
            ical.location.reservations.append(reservation)
            logging.info(log_change("ADDING", ical, reservation))
    # Reverse check reservations
    search = s.query(models.Reservation).filter_by(ical=ical).filter(models.Reservation.end >= datetime.datetime.now().date()).all()
    if len(reservations) == 0:
        search = []
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
