from helpers.icalendar.services import reduce_connection

from db import models
m = models.Ical()
m.service = 0
#m.link = "http://admin.vrbo.com/icalendar/bcc3363ffbeb4841810ea5b8f8319525.ics?nonTentative"
f = reduce_connection(m, test=True)

#print(f.reservations)

for reservation in f.reservations:
  print(reservation.guest)
  print(reservation.start)
  print(reservation.end)
  print(reservation.duration)