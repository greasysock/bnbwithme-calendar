from helpers.icalendar.assist import Connection
from db import models

class VrboConnection(Connection):
  _not_available = {'Blocked', 'Reserved'}
  _split_string = '\r\n'

  def __init__(self, ical:models.Ical, test=False):
    super().__init__(ical, test)
  
  def _process_guest(self, raw_reservation, key_value_reservation, tar_reservation:models.Reservation):
    guest_string = key_value_reservation.get('SUMMARY')
    if guest_string and guest_string not in self._not_available:
      guest_deconstruction = guest_string.split(" - ")
      if len(guest_deconstruction) == 1:
        tar_reservation.guest = guest_deconstruction[0]
      elif len(guest_deconstruction) == 2:
        tar_reservation.guest = guest_deconstruction[1]
      else:
        if guest_deconstruction[0] in self._not_available:
          return False
        raise ValueError("Guest not found in array or array is changed!")
      return True
    return False
