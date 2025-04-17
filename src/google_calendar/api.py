from core.create_file import File
from core.compare_file import CompareFiles
from google_calendar.utils import get_datetime
from core.app_state import app_state
from core.utils import stable_hash

class CalendarAPI:
    def __init__(self, calendar):
        self.logger = app_state.logger
        self.service = app_state.calendar_service
        self.calendar_data = calendar
        self.time_min, self.time_max = get_datetime()

    # Добавляет существующий календарь в список календарей пользователя
    def add_calendar(self):
        calendar_list_entry = {"id": self.calendar_data["id"]}
        try:
            self.service.calendarList().insert(body=calendar_list_entry).execute()
            self.logger.info(f"Календарь {self.calendar_data['alias']} добавлен в список.")
        except Exception as e:
            self.logger.error(f"Ошибка при добавлении календаря {self.calendar_data['alias']}: {e}")
            return

    def get_events(self):
        comparator = CompareFiles(self.calendar_data)

        if not comparator.valid: # false
            return
        else: # true
            sync_token = self.get_sync_token()
            result = comparator.compare_files(sync_token)

            if result: # Синхронизация не требуется
                return
            
        self.logger.info(f"Начинаю синхронизацию календаря {self.calendar_data['alias']}.")
        events_result = self.get_full_events()

        file_obj = File()
        file_obj.write_file(self.calendar_data, events_result)
        self.logger.info(f"События календаря {self.calendar_data['alias']} успешно записаны.")

    def get_full_events(self):
        #self.logger.debug(f"Запрашиваю события с {self.time_min} по {self.time_max}")
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
        self.logger.info(f"Запрашиваю токен синхронизации для {self.calendar_data['alias']}.")
        response_updated = self.service.events().list(
            calendarId=self.calendar_data["id"],
            maxResults=1,
            fields="updated"
        ).execute()['updated']
        return stable_hash(response_updated)