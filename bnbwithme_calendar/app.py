from db import models
from helpers.icalendar import pull as ical_pull

Session = models.session()

s = Session()

properties = s.query(models.Property).all()

for location in properties:
    for ical in location.icals:
        reservations = ical_pull.get_all_reservations(ical)
        for reservation in reservations:

            search = s.query(models.Reservation).filter_by(ical=ical).filter_by(start=reservation.start).filter_by(end=reservation.end)
            # New listing detected, add ical and add to location
            if search.first() is None:
                reservation.ical = ical
                location.reservations.append(reservation)
                print("adding")

            location.reservations.append(reservation)

    s.commit()
