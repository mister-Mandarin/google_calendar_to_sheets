from core.app_state import app_state
from dotenv import load_dotenv
from .utils import MONTHS, MONTHS_DAYS, WEEKDAYS, get_month_info
from datetime import datetime
from google_sheet.setup_new_sheet import SetupNewSheet
import os

load_dotenv()

class SheetAPI:
    def __init__(self):
        self.service = app_state.sheet_service
        self.table_id = os.getenv("TABLE_ID")
        self.logger = app_state.logger
        self.sheet = None
    
    def request(self, request):
        self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.table_id,
            body={"requests": request}
        ).execute()

    def get_list_sheets(self):
        return self.service.spreadsheets().get(
            spreadsheetId=self.table_id,
            fields="sheets.properties(sheetId,title)"
        ).execute()["sheets"]
    
    def get_month_name_from_iso(self, date_month):
        dt = datetime.strptime(date_month, "%Y-%m")
        return f"{MONTHS[dt.month]}_{dt.year}"

    def find_sheet_in_cache(self, month_name):
        #self.logger.debug(f"Поиск листа {month_name} в кэше")
        
        if month_name in app_state.sheets_cache:
            #self.logger.info(f"Лист {month_name} существует.")
            return app_state.sheets_cache[month_name]
        
        self.logger.debug(f"Лист {month_name} не существует.")
        return False
       
    def create_new_sheet(self, month_name):
        self.logger.info(f"Создаю новый лист {month_name}, перезаписываю кэш.")
        requests = [{
            "addSheet": {
                "properties": {
                    "title": month_name
                }
            }
        }]

        self.request(requests)

    def parse_sheets_to_dict(self, list_of_sheets): 
        sheets_dict = {}
        for sheet in list_of_sheets:
            try:
                props = sheet.get('properties', {})
                title = props.get('title', '')
                month = MONTHS.index(title.split("_")[0])
                year = title.split("_")[1]
                key = f"{year}-{month:02}"

                sheets_dict[key] = {
                    "sheetId": props["sheetId"],
                    "title": title
                }
            except (IndexError, ValueError):
                continue

        return sheets_dict

    def update_sheet_state(self):
        list = self.get_list_sheets()
        new_list = self.parse_sheets_to_dict(list)
        app_state._save_sheets_cache(new_list)
    
    def setup_new_sheet(self, sheet):
        self.logger.info(f"Настраиваю новый лист {sheet['title']}")

        setup = SetupNewSheet(sheet['sheetId'])
        setup.first_setup_sheet()
        self.request(setup.requests_first)

        # Узнать месяц, первый день недели, количество дней
        month = MONTHS_DAYS[MONTHS.index(sheet['title'].split("_")[0])]
        first_weekday_number, total_days = get_month_info(sheet['title'])

        for i in range(total_days):
            day_number = i + 1
            weekday_name = WEEKDAYS[(first_weekday_number + i) % 7]
            full_day_string = f"{day_number} {month}, {weekday_name}"
            start_row = 1 + (i * 30)
            setup.second_setup_sheet(start_row, full_day_string)

        self.request(setup.requests_second)

    def get_sheet_id(self, month_name):
        find_sheet = self.find_sheet_in_cache(month_name)

        if find_sheet:
            return

        name = self.get_month_name_from_iso(month_name)
        self.create_new_sheet(name)
        self.update_sheet_state()
        sheet = self.find_sheet_in_cache(month_name)
        self.setup_new_sheet(sheet)