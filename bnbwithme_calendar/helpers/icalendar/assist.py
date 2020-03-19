import requests, datetime
from db import models
from typing import List

class Connection:
  _not_available = {}
  _split_string = '\n'
  _ical_condition = "BEGIN:VCALENDAR"
  _headers = {'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

  def __init__(self, ical: models.Ical, test=False):
    self.__alive:bool = False
    self.__ical:models.Ical = ical
    self.__reservations:List[models.Reservation] = []
    self.__test = test
    self._get_reservations()
    self._content = None

  def _test_alive(self):
    if self._content:
      self.__alive = self._content[0:15] == self._ical_condition

  def _get_reservations(self):
    self._content = self.__get_raw_ical()
    self._test_alive()
    return []

  def __get_raw_ical(self):
    if not self.__test:
      r = requests.get(self.ical.url, headers=self._headers)
      if r.ok:
        return r.content.decode('utf-8')
      return False
    return open('vrbotest.ics', 'r').read()

  @property
  def alive(self):
    return self.__alive

  @property
  def ical(self):
    return self.__ical
