# -*- coding: utf-8 -*-
"""
Modified on Sun Jul  2 17:35:03 2017
@author: Paul Nunez
Now able to handle events with no body
"""

###Template engine for TSF website
### written by: Magnus Haw
### created: Oct. 14, 2014
### last modified: Nov. 18, 2014
import datetime
from functools import partial
from ReadEvents import checkCalendar

cal_names = 'calendars.txt'
recipients_file = 'recipients.txt'
login_file = 'login.txt'

###Calendars of interest
with open(cal_names, 'r') as fin:
    cal_ids = fin.read().split('\n')

###Recipients file
with open(recipients_file,'r') as fin:
    to_list = fin.read().split('\n')

#for testing purposes only
#string_date = "2017-07-16"
#date = datetime.datetime.strptime(string_date, "%Y-%m-%d").date()


###Check calendar events
date = datetime.datetime.today().date()
map(partial(checkCalendar, today = date), cal_ids, to_list)
print('Email reminders completed for today')
