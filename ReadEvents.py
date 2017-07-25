# Refer to the Python quickstart on how to setup the environment:
# https://developers.google.com/google-apps/calendar/quickstart/python
# Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
# stored credentials.


from __future__ import print_function
import httplib2

from apiclient import discovery
from oauth2client import tools
import datetime
from email_handler import Class_eMail
from get_credentials import get_credentials

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'
    
def checkCalendar(calendarId, Receiving_Email, today = datetime.date.today()):
    """
    Boiler plate code to retreive all the events in a particular day and send 
    the info to a specified email address.    
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    
    page_token = None
    allEvents = []
    while True:
      events = service.events().list(calendarId=calendarId, pageToken=page_token).execute()
      events['items'] = events['items'][::-1]
      for event in events['items']:
          try:
              string_date = str(event['start']['dateTime'].split('T')[0])
              date = datetime.datetime.strptime(string_date, "%Y-%m-%d").date()
              diff = (date-today).days
              if(diff > 0): #if in the future then it's not time to publish
                  'event is in the future, do nothing'
#                  print('event in the future', diff)
              elif(diff == 0): #if the event is today then it's time publish
                                    
                  subject = str(event['summary'])
                  email = Class_eMail()
                  try:
                      body = str(event['description'])
                      email.send_Text_Mail(Receiving_Email, subject, body)
                  except:
                      start = event['start']['dateTime'].split('T')[1].split('-')[0].rsplit(':',1)[0]
                      start = str(start)
                      end = event['end']['dateTime'].split('T')[1].split('-')[0].rsplit(':',1)[0]
                      end = str(end)
                      subject = subject + ' (Time: ' + start + ' - ' + end +')'
                      email.send_Text_Mail(Receiving_Email, Subject = subject, txtMessage = '')
                  print('email sent!')
              else: #if the event is in the past then we're done because the rest are too
                  'event is in the past, do nothing'
#                  print('event in the past', diff)
#                  break
          except:
              'do nothing'
      page_token = events.get('nextPageToken')
      if not page_token:
        break
    return allEvents

##test event
#if __name__ == '__main__':
#    string_date = "2017-07-19"
#    date = datetime.datetime.strptime(string_date, "%Y-%m-%d").date()
#    calendarId = 'calendarID@group.calendar.google.com'
#    out = checkCalendar(calendarId=calendarId, 
#                        Receiving_Email = 'example@gmail.com', today = date)
