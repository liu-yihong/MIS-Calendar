from ics import Calendar, Event
from ics.grammar.parse import ContentLine
from datetime import datetime as dt
from dateutil import tz
import pandas as pd

if __name__ == '__main__':
    c = Calendar()
    e = Event()
    e.name = 'Test'
    e.begin = dt(2019, 1, 1, 0, 0, 0, 0, tz.tzlocal())
    e.end = dt(2019, 1, 1, 0, 0, 0, 0, tz.tzlocal())
    c.events.add(e)
    print(c.events)
    
    with open('MISConferenceCalendar.ics', 'w') as my_file:
    my_file.write(str(c))