from datetime import datetime
from core.app_state import app_state
from google_sheet.api import SheetAPI
from dateutil.relativedelta import relativedelta
import json

class CheckSheetId:
    def __init__(self, alias):
        """
        sheet_data все данные с календаря по alias
        self.sheet_ragne = ['2025-04-25T10:00:00+03:00', '2025-05-01T10:00:00+03:00', '2025-06-20T20:30:00+03:00']...
        """
        self.sheet_name = alias
        self.sheet_data = self.get_sheet_items()
        self.sheet_dates_ragne = self.get_range_dates()

    def generate_months(self, start_date, end_date):
        """
        Формирую список дат. Дата начала, даты между ними, дата конца  
        Важно! Дата конца включена 2 раза, начало месяца, и сама дата конца
        Это нужно для правильного вычисления координат очистки "сверху вниз"
        """
        months = [start_date.isoformat()]
        
        current = (start_date.replace(day=1) + relativedelta(months=1))
        
        while (current.year, current.month) <= (end_date.year, end_date.month):
            months.append(current.replace(day=1, hour=9, minute=0).isoformat())
            current += relativedelta(months=1)

        months.append(end_date.isoformat())
        return months

    def get_range_dates(self):
        if not self.sheet_data:
            raise ValueError("Список items пуст.")

        start_times = [datetime.fromisoformat(event["start"]) for event in self.sheet_data]
        end_times = [datetime.fromisoformat(event["end"]) for event in self.sheet_data]

        earliest = min(start_times)
        latest = max(end_times)

        return self.generate_months(earliest, latest)
    
    def get_sheet_items(self):
        list_files = list(app_state.data_dir.glob(f"{self.sheet_name}_*.json"))

        with open(list_files[0], 'r', encoding='utf-8') as f:
            return json.load(f).get("items", [])
        
    def check_sheets_id(self):
        """
        Ищем даты в таблице, если нет - создаем
        """
        sheet_id = SheetAPI()

        for date in self.sheet_dates_ragne:
            sheet_id.get_sheet_id(date[:7])