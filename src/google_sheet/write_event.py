from datetime import datetime
from core.app_state import app_state

TIME_START = 9  # начиная с 9:00
TIME_END = 23 # до 23:00
SLOTS_PER_HOUR = 2  # по 30 минут
ROWS_PER_DAY = (TIME_END - TIME_START) * SLOTS_PER_HOUR  # 28 строк
ROW_BASE = 2  # первая строка таблицы — вторая (1 — заголовки)

class WriteEvent:
    def __init__(self):
        self.service = app_state.sheet_service
        self.logger = app_state.logger
        self.request = []

    def request(self, request):
        self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.table_id,
            body={"requests": request}
        ).execute()

    def get_row_range(dt_start, dt_end):
        # Ограничения по времени для таблицы
        effective_start = max(dt_start.hour + dt_start.minute / 60, TIME_START)
        effective_end = min(dt_end.hour + dt_end.minute / 60, TIME_END)

        # Рассчитываем смещение в строках
        day_offset = (dt_start.day - 1) * ROWS_PER_DAY + ROW_BASE

        # Расчёт слотов по округлённым значениям для координат таблицы
        start_slot = int((effective_start - TIME_START) * SLOTS_PER_HOUR)
        end_slot = int((effective_end - TIME_START) * SLOTS_PER_HOUR)

        row_start = day_offset + start_slot
        row_end = day_offset + end_slot

        return row_start, row_end

    def format_event_text(dt_start, dt_end):
        return f"{dt_start.strftime('%H:%M')}-{dt_end.strftime('%H:%M')}\nЗанято"

    def get_cell_color(self):
        rgb_hex = "FF0000"  # Красный цвет в формате HEX
        return {
            "red": int(rgb_hex[0:2], 16) / 255,
            "green": int(rgb_hex[2:4], 16) / 255,
            "blue": int(rgb_hex[4:6], 16) / 255
        }

    def write_event_block(self, date, column):
        
        start = datetime.fromisoformat(date['start'])
        end = datetime.fromisoformat(date['end'])

        text = self.format_event_text(start, end)

        row_start, row_end = self.get_row_range(start, end)
        

        self.request.append(
            {
                "mergeCells": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": row_start,
                        "endRowIndex": row_end,
                        "startColumnIndex": column,
                        "endColumnIndex": column + 1,
                    },
                    "mergeType": "MERGE_ALL",
                }
            },
            {
                "updateCells": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": row_start,
                        "endRowIndex": row_end,
                        "startColumnIndex": column,
                        "endColumnIndex": column + 1,
                    },
                    "rows": [
                        {
                            "values": [
                                {
                                    "userEnteredValue": {"stringValue": text},
                                    "userEnteredFormat": {
                                        "horizontalAlignment": "CENTER",
                                        "verticalAlignment": "MIDDLE",
                                        "wrapStrategy": "WRAP"
                                    },
                                }
                            ]
                        }
                    ] * (row_end - row_start),
                    "fields": "userEnteredValue,userEnteredFormat",
                }
            }
        )

