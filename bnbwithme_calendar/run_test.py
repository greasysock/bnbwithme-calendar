from helpers.icalendar.assist import Connection
from db import models
m = models.Ical()
f = Connection(m, test=True)

print(f.alive)