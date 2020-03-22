from typing import Dict
from ...assist import Connection
from ..vrbo import VrboConnection
from ..airbnb import AirbnbConnection
from faker import Faker
import datetime
from dateutil.relativedelta import relativedelta
from enum import Enum
import random

fake = Faker(['en_US', 'ja_JP', 'zh_TW', 'es_MX', 'fr_FR'])

class ReservationType(Enum):
  PAST = 0
  FUTURE = 1
  FUTURE_PAST = 2

class FakeReservation:
  _today = datetime.date.today()
  _parent_connection = Connection

  # Types: past, future, future_past
  def __init__(self, reservation_type:ReservationType, blocked = False):
    self._guest = self._gen_guest(blocked)
    self._blocked = blocked
    reservation_type_switch = {
      ReservationType.PAST: self._gen_start_end_past,
      ReservationType.FUTURE: self._gen_start_end_future,
      ReservationType.FUTURE_PAST: self._gen_start_end_future_past
    }
    self._reservation_type = reservation_type
    self._start, self._end = reservation_type_switch[reservation_type]()
    self.raw_reservation = self.render_raw_reservation()

  def _render_guest_ics(self):
    return f'SUMMARY:{self._guest}'

  def format_date(self, date):
    return date.strftime("%Y%m%d")

  def _render_start_ics(self):
    return f'{self._parent_connection._start_date}:{self.format_date(self._start)}'

  def _render_end_ics(self):
    return f'{self._parent_connection._end_date}:{self.format_date(self._end)}'

  # Generate list of reservation after parse
  def render_raw_reservation(self):
    out = []
    out.append(self._render_guest_ics())
    out.append(self._render_start_ics())
    out.append(self._render_end_ics())
    return out

  def key_value_pair(self):
    # Use method already available in Connection class
    return self._parent_connection._recover_reservation_key_values(self.raw_reservation)

  def _gen_guest(self, blocked):
    if blocked:
      return random.choice(list(self._parent_connection._not_available))
    return fake.name()

  def _gen_start_end_past(self):
    start = fake.date_between_dates(self._today - relativedelta(years=1), self._today - datetime.timedelta(days = 11))
    end = fake.date_between_dates(start + datetime.timedelta(days=1), start + datetime.timedelta(days=9))
    return start, end

  def _gen_start_end_future(self):
    start = fake.date_between_dates(self._today + relativedelta(days=1), self._today + relativedelta(years=1))
    end = fake.date_between_dates(start + datetime.timedelta(days=1), start + datetime.timedelta(days=9))
    return start, end

  def _gen_start_end_future_past(self):
    end = fake.date_between_dates(self._today + relativedelta(days=1), self._today + relativedelta(days=3))
    start = fake.date_between_dates(self._today - relativedelta(days=3), self._today - relativedelta(days=1))
    return start, end

class FakeAirbnbReservation(FakeReservation):
  _parent_connection = AirbnbConnection
  def __init__(self, reservation_type:ReservationType, blocked = False, privacy = False):
    self._privacy = privacy
    super().__init__(reservation_type, blocked)

  def _render_guest_ics(self):
    if self._privacy:
      return 'SUMMARY:Reserved'
    return f'SUMMARY:Airbnb ({self._guest})'

class FakeVrboReservation(FakeReservation):
  _parent_connection = VrboConnection

  def _render_guest_ics(self):
    if self._guest in self._parent_connection._not_available:
      return f'SUMMART:{self._guest}'
    return f'SUMMARY:Reserved - {self._guest}'