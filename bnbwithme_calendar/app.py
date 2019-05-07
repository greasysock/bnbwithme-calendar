from db import models
from helpers.icalendar import pull as ical_pull
import datetime, time
Session = models.session()

s = Session()

# Only sync 3 at a time.
icals = s.query(models.Ical).order_by(models.Ical.updated_at).limit(3)
for ical in icals:
    reservations = ical_pull.get_all_reservations(ical)
    for reservation in reservations:

        search = s.query(models.Reservation).filter_by(ical=ical).filter_by(start=reservation.start).filter_by(end=reservation.end)
        # New listing detected, add ical and add to location
        if search.first() is None:
            reservation.ical = ical
            ical.location.reservations.append(reservation)
            print("adding")
    ical.updated_at = datetime.datetime.utcnow()
    s.commit()
    print(ical.updated_at)