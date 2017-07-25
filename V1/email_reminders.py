# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 17:35:03 2017

@author: p
"""

###Template engine for TSF website
### written by: Magnus Haw
### created: Oct. 14, 2014
### last modified: Nov. 18, 2014
from sys import path
from util import send_mail_smtp
import datetime
import urllib2

cal_names = 'calendars.txt'
links_name = 'calendar_links.txt'
recipients_file = 'recipients.txt'
login_file = 'login.txt'

def download_cal(url,fname):
    try:
        response = urllib2.urlopen(url)
        calendar = response.read()
        fout = open(fname,'w')
        fout.write(calendar)
        fout.close()
    except:
        print 'Could not download %s calendar'%fname

###Calendars of interest
fin = open(cal_names,'r')
icsfiles = fin.read().replace('\r','').split('\n')
fin.close()

###Recipients file
fin = open(recipients_file,'r')
to_list = fin.read().split('\n')
fin.close()
print to_list

###Login file
fin = open(login_file,'r')
login = fin.read().split('\n')
sender = login[0]
host = login[1]
port = int(login[2])
username = login[3]
password = login[4]
fin.close()

####Download calendars
fin = open(links_name, 'r')
urls = fin.read().split('\n')
fin.close()
for i in range(0,len(urls)):
    download_cal(urls[i],icsfiles[i])


###Load calendar events
dtstart = datetime.datetime.today()
upcoming =[]
for j in range(0,len(icsfiles)):
    icsfile = icsfiles[j]
    print 'Parsing %s...'%icsfile
    events  = parse_ics(icsfile)

    for i in range(0,len(events)):
        next_date = get_next_date(dtstart,events[i].rrule)
        if next_date != None and (next_date.date() -dtstart.date()).days ==1:
print events[i].summary, next_date
subject = 'test'
body = 'test body'

send_mail_smtp(sender, to_list, subject, body, host, port, username, password)
print 'Sent email!'
print '\n'

