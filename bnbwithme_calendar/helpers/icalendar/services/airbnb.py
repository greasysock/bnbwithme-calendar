from helpers.icalendar.assist import Connection
from db import models

class AirbnbConnection(Connection):
  _not_available = {'Not available', '(no email alias available)'}

  def __init__(self, ical:models.Ical):
    super().__init__(ical)

