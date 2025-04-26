from dotenv import load_dotenv
from .utils import get_count_days
from dateutil.parser import isoparse
from .config_sheet import ConfigSheet
load_dotenv()

class CleanSheet(ConfigSheet):
    def __init__(self, alias):
        super().__init__(alias)
 
    def create_clean_request(self, row_start, row_end, sheet_id):
        # 1) unmerge
        self.requests.append({
            "unmergeCells": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": row_start,
                    "endRowIndex": row_end,
                    "startColumnIndex": self.first_col,
                    "endColumnIndex": self.last_col
                }
            }
        })

        # 2) clear values + background
        self.requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": row_start,
                    "endRowIndex": row_end,
                    "startColumnIndex": self.first_col,
                    "endColumnIndex": self.last_col
                },
                "cell": {
                    "userEnteredValue": {},
                    "userEnteredFormat": {
                        "backgroundColor": {"red": 1, "green": 1, "blue": 1}
                    }
                },
                "fields": "userEnteredValue,userEnteredFormat.backgroundColor"
            }
        })

    def clean_until(self, date_start, date_end, sheet_id):
        """
        dt_start:   ISO-строка даты, с которой начинаем очистку
        count_days: количество дней ДО КОНЦА МЕСЯЦА
        """
        count_days = get_count_days(date_start, date_end)
        base_row = self.first_row_of_day(isoparse(date_start))

        for i in range(count_days):
            row_start = base_row + i * self.ROWS_PER_DAY 
            row_end = row_start + self.ROWS_PER_DAY - 1
            self.create_clean_request(row_start, row_end, sheet_id)
        
        # Выполняем новый запрос для каждого листа
        self.run_request()
        self.reset_requests()