from .utils import get_index_column_by_alias
from core.app_state import app_state
import os

class ConfigSheet:
    TIME_START = 9  # начиная с 9:00
    TIME_END = 23 # до 23:00
    SLOTS_PER_HOUR = 2  # по 30 минут
    ROW_BASE = 2  # первая строка таблицы — вторая (1 — заголовки)
    # 28 строк время, + 2 строки заголовок даты
    ROWS_PER_DAY = (TIME_END - TIME_START) * SLOTS_PER_HOUR + ROW_BASE

    def __init__(self, alias):
        """
        table_id: ID таблицы
        first_col, last_col индексы столбца календаря
        requests: список запросов для очистки
        """
        self.service = app_state.sheet_service
        self.table_id = os.getenv("TABLE_ID")
        self.first_col, self.last_col, self.colors = get_index_column_by_alias(alias)
        self.logger = app_state.logger
        self.requests = []

    def run_request(self):
        #self.logger.info(f"Запрос для таблицы {self.table_id}: {self.requests}.")
        self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.table_id,
            body={"requests": self.requests}
        ).execute()

    def first_row_of_day(self, dt) -> int:
        return self.ROW_BASE + (dt.day - 1) * self.ROWS_PER_DAY
    
    def reset_requests(self):
        self.requests = []
    