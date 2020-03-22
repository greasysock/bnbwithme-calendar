from db import models
from .example_ics_builder import ReservationType, FakeAirbnbReservation
from ..airbnb import AirbnbConnection

def test_guest_parse():
  reservation = models.Reservation()
  for _ in range(1000):
    f = FakeAirbnbReservation(ReservationType.PAST)
    valid = AirbnbConnection._process_guest(f.raw_reservation, f.key_value_pair(), reservation)
    assert reservation.guest == f._guest
    assert valid

def test_guest_private_parse():
  reservation = models.Reservation()
  for _ in range(100):
    f = FakeAirbnbReservation(ReservationType.PAST, privacy=True)
    valid = AirbnbConnection._process_guest(f.raw_reservation, f.key_value_pair(), reservation)
    assert reservation.guest == 'Reserved'
    assert valid

def test_guest_blocked():
  reservation = models.Reservation()
  for _ in range(100):
    f = FakeAirbnbReservation(ReservationType.PAST, blocked=True)
    valid = AirbnbConnection._process_guest(f.raw_reservation, f.key_value_pair(), reservation)
    assert not valid
