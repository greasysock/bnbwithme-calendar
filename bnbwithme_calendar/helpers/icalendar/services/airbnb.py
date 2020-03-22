from helpers.icalendar.assist import Connection
from db import models
import re

class AirbnbConnection(Connection):
  _not_available = {'Not available'}

  def __init__(self, ical:models.Ical):
    super().__init__(ical)
  
  @classmethod
  def _process_guest(self, raw_reservation, key_value_reservation, tar_reservation:models.Reservation):
    guest_string = key_value_reservation.get('SUMMARY')
    if guest_string == 'Reserved':
      tar_reservation.guest = guest_string
      return True
    else:
      guest_search = re.search('Airbnb \((.*)\)', guest_string, re.IGNORECASE)
      if guest_search and guest_search.group(1) and guest_search.group(1) not in self._not_available:
        tar_reservation.guest = guest_search.group(1)
        return True
    return False
