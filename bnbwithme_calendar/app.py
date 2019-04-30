from db import models

Session = models.session()

s = Session()

properties = s.query(models.Property).all()

for location in properties:
    for ical in location.icals:
        print(ical.link)
    print(location.name)
