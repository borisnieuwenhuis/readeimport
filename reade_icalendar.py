# imports
from icalendar import Calendar, Event, vCalAddress, vText
from datetime import datetime, timedelta
from pytz import timezone

from pathlib import Path
import os
import pytz
import csv

# init the calendar
cal = Calendar() 

# Some properties are required to be compliant
cal.add('prodid', '-//My calendar product//example.com//')
cal.add('version', '2.0')

DATE_FORMAT = "%d-%m-%Y %H:%M"

with open('input', newline='') as csvfile:
	spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
	for row in spamreader:

		# Add subcomponents
		event = Event()
		event.add('summary', "%s: %s" % (row[3], row[4]))
		event.add('description', row[-3])

		start = datetime.strptime("%s %s" % (row[1], row[2]), DATE_FORMAT).replace(tzinfo=timezone('CET'))
		event.add('dtstart', start)
		event.add('dtend', start + timedelta(minutes=30))
		
		attendee = vCalAddress('MAILTO:borisnieuwenhuis@gmail.com')
		attendee.params['name'] = vText('Boris Nieuwenhuis')
		attendee.params['role'] = vText('REQ-PARTICIPANT')
		event.add('attendee', attendee, encode=0)

		# Add the organizer
		organizer = vCalAddress('MAILTO:%s' % row[4].replace(" ", "_"))
		 
		# Add parameters of the event
		organizer.params['name'] = vText(row[2])
		organizer.params['role'] = vText(row[3])
		print(organizer)
		event['organizer'] = organizer

		event['location'] = vText('Overtoom 283, 1054 HW Amsterdam')
		event['uid'] = start
		event.add('priority', 5)
		
		# Add the event to the calendar
		cal.add_component(event)

# Write to disk
directory = Path.cwd() / 'ReadeCalendar'
try:
   directory.mkdir(parents=True, exist_ok=False)
except FileExistsError:
   print("Folder already exists")
else:
   print("Folder was created")
 
f = open(os.path.join(directory, 'example.ics'), 'wb')
f.write(cal.to_ical())
f.close()