from google_calendar.api import CalendarAPI
from google_calendar.utils import CALENDAR_LIST
from core.app_state import app_state

#calendar_data = CALENDAR_LIST[0]
def run_calendar_operations():
    for calendar_data in CALENDAR_LIST:
    #app_state.logger.debug(f"calendar_data: {calendar_data}")
        calendar = CalendarAPI(calendar_data)
        if not calendar.exists_calendar():
            calendar.add_calendar()
        calendar.get_events()