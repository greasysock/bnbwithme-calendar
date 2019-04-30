from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from db import models

e = models.connect()
session_factory = sessionmaker(bind=e)
Session = scoped_session(session_factory)

s = Session()

print(s.query(models.Property).all()[0].icals[0].site())

