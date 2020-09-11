from __future__ import print_function
from datetime import time
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pytz

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']
MONTHS = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']
DAYS = ['lunes','martes','miércoles','jueves','viernes','sábado','domingo']

def google_authentication():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service

def get_events(day, service):
    # Call the Calendar API
    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)

    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(), timeMax = end_date.isoformat(),
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events

def get_date(text):
    today = datetime.date.today()
    if "hoy" in text:
        return today
    day = -1
    day_of_week = -1
    month = -1
    year = today.year
    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
    if (month < today.month) and (month != -1):
        year = year+1
    if (day < today.day) and (month == -1) and (day != -1):
        month = month + 1
    if (month == -1) and (day == -1) and (day_of_week != -1):
        current_day_of_week = today.weekday()
        dif = day_of_week - current_day_of_week
        if dif < 0:
            dif += 7
        return today + datetime.timedelta(dif)
    if (month == -1) or (day == -1):
        return None
    return datetime.date(year=year,month=month,day=day)

def get_hour(text):
    if "am" in text:
        if ("las" in text) and ("y" in text):
            hours = int(text.split("las")[1].split("am")[0].split("y")[0])
            minutes = int(text.split("las")[1].split("am")[0].split("y")[1])
            if "media" in text:
                minutes = 30
        elif "las" in text:
            hours = int(text.split("las")[1].split("am")[0].split(":")[0])
            minutes = int(text.split("las")[1].split("am")[0].split(":")[1])
        else:
            if "y" in text:
                hours = int(text.split("am")[0].split("y")[0])
                minutes = int(text.split("am")[0].split("y")[1])
                if "media" in text:
                    minutes = 30
            else:
                if ":" in text:
                    hours = int(text.split("am")[0].split(":")[0])
                    minutes = int(text.split("am")[0].split(":")[1])
                else:
                    hours = int(text.split("am")[0])
                    minutes = 0
    if "pm" in text:
        if ("las" in text) and ("y" in text):
            hours = int(text.split("las")[1].split("pm")[0].split("y")[0])
            minutes = int(text.split("las")[1].split("pm")[0].split("y")[1])
            if "media" in text:
                minutes = 30
        elif "las" in text:
            hours = int(text.split("las")[1].split("pm")[0].split(":")[0])
            minutes = int(text.split("las")[1].split("pm")[0].split(":")[1])
        else:
            if "y" in text:
                hours = int(text.split("pm")[0].split("y")[0])
                minutes = int(text.split("pm")[0].split("y")[1])
                if "media" in text:
                    minutes = 30
            else:
                if ":" in text:
                    hours = int(text.split("pm")[0].split(":")[0])
                    minutes = int(text.split("pm")[0].split(":")[1])
                else:
                    hours = int(text.split("pm")[0])
                    minutes = 0
        hours = 12 + hours
    hora = time(hour=hours,minute=minutes)
    return hora

def create_event(service, summary, location, description, datetime, inicio, fin):
    GMT_OFF = '-05:00'
    event = {
                'summary': summary,
                'location': location,
                'description': description,
                'start': {
                    'dateTime': str(datetime)+'T'+str(inicio)+GMT_OFF,
                    'timeZone': 'America/Lima',
                },
                'end': {
                    'dateTime': str(datetime)+'T'+str(fin)+GMT_OFF,
                    'timeZone': 'America/Lima',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                    {'method': 'email', 'minutes': 30},
                    {'method': 'popup', 'minutes': 30},
                    ],
                },
            }
    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))    
    