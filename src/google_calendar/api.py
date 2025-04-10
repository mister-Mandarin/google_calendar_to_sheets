from core.create_file import File
from core.compare_file import CompareFiles
from google_calendar.utils import get_datetime
from core.app_state import app_state

class CalendarAPI:
    def __init__(self, calendar):
        self.service = app_state.calendar_service
        self.calendar_data = calendar
        self.time_min, self.time_max = get_datetime()

    # Добавляет существующий календарь в список календарей пользователя
    def add_calendar(self):
        calendar_list_entry = {"id": self.calendar_data["id"]}
        try:
            self.service.calendarList().insert(body=calendar_list_entry).execute()
        except Exception as e:
            print(e)

    def get_events(self):

        comparator = CompareFiles(self.calendar_data)

        if not comparator.valid: # false
            return
        else: # true
            sync_token = self.get_sync_token()
            result = comparator.compare_files(sync_token)

            if result: # not sync yet
                return
            
        print('need sync and write')
        events_result = self.get_full_events()

        file_obj = File()
        file_obj.write_file(self.calendar_data, events_result)

    def get_full_events(self):
        return self.service.events().list(
        calendarId=self.calendar_data["id"],
        timeMin=self.time_min,
        timeMax=self.time_max,
        maxResults=2, #!!!!!!
        singleEvents=True,
        orderBy="startTime",
        fields="updated, items(id, start/dateTime, end/dateTime)",
        ).execute()
    
    def get_sync_token(self):
        return hash(
                self.service.events().list(
                calendarId=self.calendar_data["id"],
                maxResults=1, 
                fields="updated"
                ).execute()['updated']
        )