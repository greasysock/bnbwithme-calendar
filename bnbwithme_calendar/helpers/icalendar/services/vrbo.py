from helpers.icalendar.assist import Connection
from db import models

class VrboConnection(Connection):
  _not_available = {'Blocked'}
  _split_string = '\r\n'

  def __init__(self, ical:models.Ical):
    super().__init__(ical)

