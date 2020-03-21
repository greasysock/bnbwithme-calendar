from . import airbnb, vrbo
from db import models

ical_reduction = {
  0: airbnb.AirbnbConnection,
  1: vrbo.VrboConnection
}

def reduce_connection(ical:models.Ical, test=False):
  return ical_reduction[ical.service](ical, test)
