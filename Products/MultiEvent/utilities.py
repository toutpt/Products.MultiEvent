## event utilities
from DateTime import DateTime

def isEmptyEvent(event):
    if event['startDate']=='' and \
       event['endDate']=='' and \
       event['location']=='':
        return True
    else:
        return False

def isValidEvent(event):
    if not event['location']:
        return False

    start = event['startDate']
    if start:
        try:
            DateTime(start)
        except:
            return False
    else:
        return False

    end = event['endDate']
    if end:
        try:
            DateTime(end)
        except:
            return False
    else:
        return False

    # start < end

    return True

def clear_from_invalid_events(events):
    return [event for event in events if isValidEvent(event)]

date_format = '%d/%m/%Y'
def date_in_formatted_string_format(date):
    return date.strftime(date_format)

def date_components(date):
    if ' ' in date:
        date, time = date.split(' ')
    day, month, year = date.split('/')
    return (int(year), int(month), int(day))

def DateTimeFromFormattedString(date, time=''):
    date_c = date_components(date)
    if time:
        time_c = tuple(map(int, time.split(":")))
        components = date_c + time_c
        return DateTime(*components)
    else:
        return DateTime(*date_c)
