import requests, datetime
from db import models

def get_raw_ical(link):
    #r = requests.get(link)
    #return r.content.decode('utf-8')
    return open('abbtest.ics', 'r').read()

# Returns array split by BEGIN/END
def get_raw_split_ical(link):
    tmpraw = get_raw_ical(link).split('\\n')
    raw = []
    for line in tmpraw:
        raw += line.split('\n')
    begin_event = "BEGIN:VEVENT"
    end_event = "END:VEVENT"
    split_event = []
    def get_all_split_events(split_event, cursor):
        if cursor == raw.__len__()-1:
            return split_event
        if raw[cursor] == begin_event:
            start_idx = cursor + 1
            while True:
                cursor += 1
                if raw[cursor] == end_event:
                    split_event.append(raw[start_idx:cursor])
                    break

        cursor += 1
        return get_all_split_events(split_event, cursor)
    split = get_all_split_events(split_event, 0)
    return split
    
def recover_values(recover:tuple, source:list):
    out = []
    temp_types = dict()
    # n+m solution
    # Create map for potential recoveries
    for row in source:
        s = row.split(":")
        if s.__len__() > 1:
            temp_types[s[0]] = s[1]
    # Map recovered values to respective targets
    for target_recover in recover:
        if target_recover in temp_types:
            out.append(temp_types[target_recover])
        else:
            out.append(None)
    return out

def recover_date(date_string : str):
    return datetime.datetime.strptime(date_string, "%Y%m%d").date()

def get_all_airbnb_reservations(ical : models.Ical):
    split_list = get_raw_split_ical(ical.link)
    find = ("DTSTART;VALUE=DATE", "DTEND;VALUE=DATE", "SUMMARY", "EMAIL")
    out_reservations = []
    for event in split_list:
        recovered = recover_values(find, event)
        start = recover_date(recovered[0])
        if start >= datetime.datetime.now().date():
            print(start)
            reservation = models.Reservation
            reservation.start = start
            reservation.end = recover_date(recovered[1])
            reservation.ical = ical
            out_reservations.append(reservation)
    return out_reservations

def get_all_vrbo_reservations(ical : models.Ical):
    pass

def get_all_reservations(ical : models.Ical):
    if ical.site() is models.Service.airbnb:
        return get_all_airbnb_reservations(ical)
    elif ical.site() is models.Service.vrbo:
        return get_all_vrbo_reservations(ical)
    return []