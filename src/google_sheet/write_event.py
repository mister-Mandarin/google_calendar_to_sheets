from datetime import datetime
from core.app_state import app_state
from .config_sheet import ConfigSheet
import random
import json

class WriteEvent(ConfigSheet):
    def __init__(self, alias):
        super().__init__(alias)
        self.sheet_data = self.get_sheet_items(alias)

    def get_sheet_items(self, alias):
        list_files = list(app_state.data_dir.glob(f"{alias}_*.json"))

        with open(list_files[0], 'r', encoding='utf-8') as f:
            return json.load(f).get("items", [])

    def get_row_range(self, dt_start, dt_end):
        # Ограничения по времени для таблицы
        effective_start = max(dt_start.hour + dt_start.minute / 60, self.TIME_START)
        effective_end = min(dt_end.hour + dt_end.minute / 60, self.TIME_END)

        # Рассчитываем смещение в строках
        day_offset = (dt_start.day - 1) * self.ROWS_PER_DAY + self.ROW_BASE

        # Расчёт слотов по округлённым значениям для координат таблицы
        start_slot = int((effective_start - self.TIME_START) * self.SLOTS_PER_HOUR)
        end_slot = int((effective_end - self.TIME_START) * self.SLOTS_PER_HOUR)

        row_start = day_offset + start_slot
        row_end = day_offset + end_slot

        return row_start, row_end

    def format_event_text(self, dt_start, dt_end):
        return f"{dt_start.strftime('%H:%M')}-{dt_end.strftime('%H:%M')}\nЗанято"

    def get_cell_color(self):
        rgb_hex = random.choice(self.colors)
        return {
            "red": int(rgb_hex[0:2], 16) / 255,
            "green": int(rgb_hex[2:4], 16) / 255,
            "blue": int(rgb_hex[4:6], 16) / 255
        }
    
    def create_write_request(self, row_start, row_end, text, sheet_id):
            # Объединяем ячейки
            range = {
                        "sheetId": sheet_id,
                        "startRowIndex": row_start,
                        "endRowIndex": row_end,
                        "startColumnIndex": self.first_col,
                        "endColumnIndex": self.last_col,
                    }

            self.requests.append({
                "mergeCells": {
                    "range": range,
                    "mergeType": "MERGE_ALL",
                }
            })

            # Заполнение объединённого диапазона текстом, выравниванием и фоном
            cell_color = self.get_cell_color()

            self.requests.append({
                "repeatCell": {
                    "range": range,
                    "cell": {
                        "userEnteredValue": {"stringValue": text},
                        "userEnteredFormat": {
                            "backgroundColor": cell_color,
                            "horizontalAlignment": "CENTER",
                            "verticalAlignment": "MIDDLE",
                            "wrapStrategy": "WRAP"
                        }
                    },
                    "fields": "userEnteredValue,userEnteredFormat.backgroundColor,userEnteredFormat.horizontalAlignment,userEnteredFormat.verticalAlignment,userEnteredFormat.wrapStrategy"
                }
            })

    def get_id_from_cache(self, data):
        """Получить данные листа из кэша"""
        key = str(data)[:7]
        if key in app_state.sheets_cache:
            return app_state.sheets_cache[key]['sheetId']

    def setup_event_block(self, event):
        start = datetime.fromisoformat(event['start'])
        end = datetime.fromisoformat(event['end'])
        text = self.format_event_text(start, end)
        row_start, row_end = self.get_row_range(start, end)
        sheet_id = self.get_id_from_cache(start)
        
        self.create_write_request(row_start, row_end, text, sheet_id)
    

    def write_event_block(self):

        if self.sheet_data:
            for event in self.sheet_data:
                self.setup_event_block(event) 

            self.run_request()
            self.reset_requests()