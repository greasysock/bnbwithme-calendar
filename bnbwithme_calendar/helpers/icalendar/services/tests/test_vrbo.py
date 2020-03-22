from db import models
from .example_ics_builder import ReservationType, FakeVrboReservation
from ..vrbo import VrboConnection

def test_guest_parse():
  reservation = models.Reservation()
  for _ in range(1000):
    f = FakeVrboReservation(ReservationType.PAST)
    print(f.raw_reservation)
    valid = VrboConnection._process_guest(f.raw_reservation, f.key_value_pair(), reservation)
    assert reservation.guest == f._guest
    assert valid

def test_guest_blocked():
  reservation = models.Reservation()
  for _ in range(100):
    f = FakeVrboReservation(ReservationType.PAST, blocked=True)
    valid = VrboConnection._process_guest(f.raw_reservation, f.key_value_pair(), reservation)
    assert not valid
