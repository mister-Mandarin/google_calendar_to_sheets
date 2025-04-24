from datetime import datetime
from core.app_state import app_state
from dotenv import load_dotenv
from .utils import get_count_days, get_index_column_by_alias
from dateutil.parser import isoparse
import os

load_dotenv()

TIME_START = 9  # начиная с 9:00
TIME_END = 23 # до 23:00
SLOTS_PER_HOUR = 2  # по 30 минут
ROW_BASE = 2  # первая строка таблицы — вторая (1 — заголовки)
# 28 строк время, + 2 строки заголовок даты
ROWS_PER_DAY = (TIME_END - TIME_START) * SLOTS_PER_HOUR + ROW_BASE

class CleanSheet:
    def __init__(self, alias):
        """
        table_id: ID таблицы
        first_col, last_col индексы столбца календаря
        requests: список запросов для очистки
        """
        self.service = app_state.sheet_service
        self.table_id = os.getenv("TABLE_ID")
        self.first_col, self.last_col = get_index_column_by_alias(alias)
        self.requests = []

    def run_request(self):
        self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.table_id,
            body={"requests": self.requests}
        ).execute()

    def first_row_of_day(self, dt) -> int:
        return ROW_BASE + (dt.day - 1) * ROWS_PER_DAY
    
    def create_request(self, row_start, row_end, sheet_id):
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
            row_start = base_row + i * ROWS_PER_DAY 
            row_end = row_start + ROWS_PER_DAY - 1
            self.create_request(row_start, row_end, sheet_id)
        
        # Выполняем новый запрос для каждого листа
        self.run_request()
        self.requests = []
                
        
