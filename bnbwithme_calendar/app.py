from db import models
from helpers.icalendar import pull as ical_pull

Session = models.session()

s = Session()

properties = s.query(models.Property).all()

for location in properties:
    for ical in location.icals:
        reservations = ical_pull.get_all_reservations(ical)
        for reservation in reservations:
            print(reservation.start)
        print(ical.link)
    print(location.name)
    print(location.reservations)
    print(location.created_at)