from datetime import datetime
from core.app_state import app_state
from google_sheet.api import SheetAPI
from dateutil.relativedelta import relativedelta
import json

class CheckSheetId:
    def __init__(self, sheet):
        self.sheet_name = sheet
        self.sheet_data = self.get_sheet_items()

    def generate_months(self, start_date, end_date):
        months = []
        current = start_date.replace(day=1)
        while current <= end_date:
            months.append(current.strftime("%Y-%m"))
            current += relativedelta(months=1)
        
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
        range = self.get_range_dates()
        return range
        #sheet_id = SheetAPI()
        #sheet_id.get_sheet_id(earliest)
        #self.sheets_id["earliest"] = id

        