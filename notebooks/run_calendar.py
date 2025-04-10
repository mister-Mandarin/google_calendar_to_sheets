import sys
from pathlib import Path 

sys.path.append(str(Path.cwd().parent / 'src'))
from google_calendar.api import CalendarAPI
from google_calendar.utils import CALENDAR_LIST

def run_calendar_operations():
    CALENDAR = CALENDAR_LIST[0]
    calendar = CalendarAPI(CALENDAR)
    calendar.add_calendar()
    calendar.get_events()