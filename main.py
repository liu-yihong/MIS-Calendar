#!/usr/bin/env python
# -*- coding:utf-8 -*-
###
# File: main.py
# File Created: Tuesday, 18th April 2023 5:41:46 pm
# Author: Yihong Liu (https://liu-yihong.github.io/)
# -----
# Last Modified: Tuesday April 18th 2023 5:41:46 pm
# Modified By: the developer formerly known as Yihong Liu
# -----
# This Python script is used to generate a calendar file (.ics) for MIS conferences.
# Github actions will be used to automatically generate the calendar file and push it to the repository.
# The calendar file can be imported to Google Calendar, Outlook, etc.
# The repository is hosted here https://github.com/liu-yihong/MIS-Calendar
# -----
# Copyright (c) 2023 Yihong Liu
###
from ics import Calendar, Event
from ics.grammar.parse import ContentLine
from datetime import datetime as dt
from dateutil import tz
import pandas as pd

'''Utility variables and functions'''

date_format = '%Y-%m-%d %H:%M:%S'

# https://coolors.co/palette/f94144-f3722c-f8961e-f9844a-f9c74f-90be6d-43aa8b-4d908e-577590-277da1
ColorPalette = {
    'ICIS': '#F94144',
    'CIST': '#F3722C',
    'WISE': '#F8961E',
    'WITS': '#F9844A',
    'TEIS': '#F9C74F',
    'SCECR': '#90BE6D',
    'CHITA': '#43AA8B',
    'HICSS': '#4D908E',
    'CSWIM': '#577590',
    'POMS': '#277DA1'
}
DEFAULT_COLOR = '#219ebc'

if __name__ == '__main__':
    # Read conference information from a spreadsheet
    CalendarDF = pd.read_excel('ConferenceList.xlsx', keep_default_na=False)
    # Create a calendar object
    ConferenceCalendar = Calendar(creator='Yihong Liu Yihong.Liu@UTDallas.edu')
    # Add events to the calendar by iterating through the rows of the spreadsheet
    for idx, row in CalendarDF.iterrows():
        # Convert start time (local time) to UTC time
        start = row['Start']  # local time
        start_dt = dt.strptime(start, date_format).replace(
            tzinfo=tz.gettz(row['Time Zone']))  # set local time zone
        start_dt = start_dt.astimezone(tz.tzutc())  # convert it to utc
        start_dt = start_dt.strftime(date_format)
        # Convert end time (local time) to UTC time
        if row['End'] != '':
            end = row['End']  # local time
            end_dt = dt.strptime(end, date_format).replace(
                tzinfo=tz.gettz(row['Time Zone']))  # set local time zone
            end_dt = end_dt.astimezone(tz.tzutc())  # convert it to utc
            end_dt = end_dt.strftime(date_format)
        else:
            end_dt = None
        # Create an event object
        event1 = Event(
            name=row['Name'],
            begin=start_dt,
            end=end_dt,
            description=row['Description'],
            created=dt.now(),
            location=row['Location'],
            url=row['URL'],
            alarms=None,
            categories=row['Categories'].split(', '),
        )
        # event1.extra.extend([
        #     ContentLine(name='color', value=ColorPalette.get(row['Categories'].split(', ')[0], DEFAULT_COLOR)),
        #     ContentLine(name='tag', value=row['Categories'].split(', ')[0])
        # ])
        # Add the event to the calendar
        ConferenceCalendar.events.add(event1)

    # Add extra information to the calendar
    ConferenceCalendar.extra.extend([
        ContentLine(name='CALSCALE', value='GREGORIAN'),
        ContentLine(name='X-WR-CALNAME', value='MIS Conference Calendar',),
        ContentLine(name='X-WR-CALDESC',
                    value='Conference Events of Management Information Systems, hosted at https://github.com/liu-yihong/MIS-Calendar',),
        ContentLine(name='X-PUBLISHED-TTL', value='PT24H',)
    ])

    with open('MISConferenceCalendar.ics', 'w') as my_file:
        my_file.write(str(ConferenceCalendar))
