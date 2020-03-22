from helpers.icalendar.assist import Connection
from db import models
import re

class VrboConnection(Connection):
  _not_available = {'Blocked', 'Reserved'}
  _split_string = '\r\n'

  def __init__(self, ical:models.Ical):
    super().__init__(ical)
  
  @classmethod
  def _process_guest(self, raw_reservation, key_value_reservation, tar_reservation:models.Reservation):
    guest_string = key_value_reservation.get('SUMMARY')
    if guest_string and guest_string not in self._not_available:
      guest_search = re.search('Reserved - (.*)', guest_string, re.IGNORECASE)
      guest_deconstruction = guest_string.split(" - ")
      if guest_search:
        tar_reservation.guest = guest_search.group(1)
        return True
      else:
        if guest_deconstruction[0] in self._not_available:
          return False
        raise ValueError("Guest not found in array or array is changed!")
    return False
