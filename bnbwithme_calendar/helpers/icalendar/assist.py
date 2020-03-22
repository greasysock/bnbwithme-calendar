import requests, datetime
from db import models
from typing import List

class Connection:
  _not_available = {}
  _split_string = '\n'
  _ical_condition = "BEGIN:VCALENDAR"
  _begin_event = "BEGIN:VEVENT"
  _end_event = "END:VEVENT"
  _start_date = 'DTSTART;VALUE=DATE'
  _end_date = 'DTEND;VALUE=DATE'
  _headers = {'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

  def __init__(self, ical: models.Ical):
    self.__alive:bool = False
    self.__ical:models.Ical = ical
    self.__reservations:List[models.Reservation] = []
    self._content = None
    self._get_reservations()

  def _test_alive(self):
    if self._content:
      self.__alive = self._content[0:15] == self._ical_condition

  def _get_split_raw_ical(self):
    lined_block_raw = self._content.split('\\n')
    block_raw = []

    for line in lined_block_raw:
      block_raw += line.split(self._split_string)
    
    raw_reservations = []

    def get_all_split_reservations(raw_reservations, cursor):
      if cursor == block_raw.__len__()-1:
        return raw_reservations
      
      if block_raw[cursor] == self._begin_event:
        start_idx = cursor + 1
        while True:
          cursor += 1
          if block_raw[cursor] == self._end_event:
            raw_reservations.append(block_raw[start_idx:cursor])
            break
      cursor += 1
      return get_all_split_reservations(raw_reservations, cursor)

    return get_all_split_reservations(raw_reservations, 0)

  @classmethod
  def _recover_reservation_key_values(self, unp_reservation:List[str]):
    key_values = dict()
    # Create map for potential recoveries
    for entry in unp_reservation:
      s = entry.split(":")
      if s.__len__() > 1:
        key_values[s[0]] = s[1]

    return key_values
  
  @classmethod
  def _parse_date(self, date_string):
    return datetime.datetime.strptime(date_string, "%Y%m%d").date()

  # Implemented in children classes
  @classmethod
  def _process_guest(self, raw_reservation, key_value_reservation, tar_reservation):
    return False

  @classmethod
  def _process_start(self, raw_reservation, key_value_reservation, tar_reservation):
    start_date_string = key_value_reservation.get(self._start_date)
    if start_date_string:
      start_date = self._parse_date(start_date_string)
      tar_reservation.start = start_date
      return True

    return False

  @classmethod
  def _process_end(self, raw_reservation, key_value_reservation, tar_reservation):
    end_date_string = key_value_reservation.get(self._end_date)
    if end_date_string:
      end_date = self._parse_date(end_date_string) + datetime.timedelta(days=1)
      if end_date >= datetime.datetime.now().date():
        tar_reservation.end = end_date
        return True
    return False

  def _process_duration(self, tar_reservation:models.Reservation):
    tar_reservation.duration = int((tar_reservation.end - tar_reservation.start).days)

  def _process_raw_reservation(self, raw_reservation):
    reservation = models.Reservation()
    key_value_reservation = self._recover_reservation_key_values(raw_reservation)
    # Pull name
    if not self._process_guest(raw_reservation, key_value_reservation, reservation): return False
    # Pull start
    if not self._process_start(raw_reservation, key_value_reservation, reservation): return False
    # Pull end
    if not self._process_end(raw_reservation, key_value_reservation, reservation): return False

    self._process_duration(reservation)
    # ... Implement any special extraction in service class by defining function and calling super() to ensure base process is executed
    return reservation

  def _get_reservations(self):
    self._content = self.__get_raw_ical()
    self._test_alive()
    if not self.alive: return []

    raw_reservations = self._get_split_raw_ical()

    for raw_reservation in raw_reservations:
      reservation = self._process_raw_reservation(raw_reservation)
      if reservation: self.__reservations.append(reservation)
    return self.__reservations

  def __get_raw_ical(self):
    r = requests.get(self.ical.link, headers=self._headers)
    if r.ok:
      return r.content.decode('utf-8')
    return False

  @property
  def alive(self):
    return self.__alive

  @property
  def ical(self):
    return self.__ical
  
  @property
  def reservations(self):
    return self.__reservations
