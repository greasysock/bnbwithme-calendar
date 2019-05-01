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

def abb_recover_itinerary(guest_string : str):
    # New abb parse method
    start_index = None
    end_index = None
    for n, letter in enumerate(guest_string):
        if letter == "(":
            start_index = n+1
    if not start_index:
        return 'Not available'
    for m, letter in enumerate(guest_string[start_index:]):
        m = m+start_index
        if letter == ")":
            end_index = m
    if not start_index:
        return 'Not available'
    return guest_string[start_index:end_index]

abb_not_available = {'Not available', "(no email alias available)"}

def abb_recover_guest(guest_string : str):
    return guest_string.split('(')[0][:-1]

def abb_recover_email(email_string : str):
    whitespace_free_email = email_string.strip()
    if whitespace_free_email in abb_not_available:
        return None
    return whitespace_free_email

def abb_recover_phone(event_list : list):
    abb_phone = "PHONE: "
    for i, event in enumerate(event_list):
        if event == abb_phone:
            number = event_list[i+1].strip()
            if number != "":
                return number
    return None

def get_all_airbnb_reservations(ical : models.Ical):
    split_list = get_raw_split_ical(ical.link)
    find = ("DTSTART;VALUE=DATE", "DTEND;VALUE=DATE", "SUMMARY", "EMAIL")
    out_reservations = []
    for event in split_list:
        recovered = recover_values(find, event)
        start = recover_date(recovered[0])
        end = recover_date(recovered[1])
        guest_check = abb_recover_itinerary(recovered[2])
        # Only deal with upcoming or current reservations
        if (start >= datetime.datetime.now().date() or end >= datetime.datetime.now().date()) and (guest_check not in abb_not_available):
            reservation = models.Reservation()
            reservation.start = start
            reservation.end = end
            reservation.guest = abb_recover_guest(recovered[2])
            reservation.email = abb_recover_email(recovered[3])
            reservation.phone = abb_recover_phone(event)
            # Create Time delta and convert into days int
            reservation.duration = int((reservation.end - reservation.start).days)
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