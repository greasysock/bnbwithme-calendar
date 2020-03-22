from pytest_localserver import http
import os
import datetime
from helpers.icalendar.assist import Connection
from db.models import Ical, Reservation
from .example_ics_builder import FakeReservation, ReservationType

def get_file(relative_path):
  dirname = os.path.dirname(__file__)
  filename = os.path.join(dirname, relative_path)
  return open(filename).read()

def build_test_ical(content:str):
  t = Ical()
  s = http.ContentServer()
  s.serve_content(content)
  s.start()
  t.link = s.url
  return t, s

def test_if_can_determine_not_alive_by_empty_and_200():
  test_ical, s = build_test_ical('')
  test_connection = Connection(test_ical)
  assert not test_connection.alive
  s.stop()

def test_if_can_determine_alive_by_valid_ical():
  test_ical, s = build_test_ical('BEGIN:VCALENDAR')
  test_connection = Connection(test_ical)
  assert test_connection.alive
  s.stop()

def test_start_date_parse():
  reservation = Reservation()
  for _ in range(100):
    f = FakeReservation(ReservationType.PAST)
    valid = Connection._process_start(f.raw_reservation, f.key_value_pair(), reservation)
    assert f._start == reservation.start
    assert valid

def test_end_date_parse():
  reservation = Reservation()
  for _ in range(100):
    f = FakeReservation(ReservationType.FUTURE)
    valid = Connection._process_end(f.raw_reservation, f.key_value_pair(), reservation)
    assert f._end + datetime.timedelta(days = 1) == reservation.end
    assert valid

def test_past_end_date():
  reservation = Reservation()
  for _ in range(100):
    f = FakeReservation(ReservationType.PAST)
    valid = Connection._process_end(f.raw_reservation, f.key_value_pair(), reservation)
    assert not valid

def test_future_past_end_date():
  reservation = Reservation()
  for _ in range(100):
    f = FakeReservation(ReservationType.FUTURE_PAST)
    valid = Connection._process_end(f.raw_reservation, f.key_value_pair(), reservation)
    assert f._end + datetime.timedelta(days = 1) == reservation.end
    assert valid
