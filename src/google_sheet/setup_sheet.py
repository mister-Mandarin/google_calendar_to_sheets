
from google_calendar.utils import CALENDAR_LIST
from core.app_state import app_state
from google_sheet.utils import MONTHS, TIME_INTERVAL, get_month_info

class SetupSheet:
    def __init__(self):
        self.sheet_id = 1165124638
        self.requests = []

    # 
    def first_setup_sheet(self):
        # скрыть столбцы !(с 7 по 27 в интерфейсе)
        self.requests.append({
            'updateDimensionProperties': {
                "range": {
                    "sheetId": self.sheet_id,
                    "dimension": 'COLUMNS',
                    "startIndex": 6,
                    "endIndex": 26,
                },
            "properties": {
                "hiddenByUser": True,
            },
            "fields": 'hiddenByUser',
        }})

        # выставляем шиирну столбцов
        for i in range(0, CALENDAR_LIST.__len__() + 1):
            self.requests.append({
                'updateDimensionProperties': {
                    "range": {
                        "sheetId": self.sheet_id,
                        "dimension": 'COLUMNS',
                        "startIndex": i,
                        "endIndex": i + 1,
                    },
                    "properties": {
                        "pixelSize": 40 if i == 0 else 155,
                    },
                    "fields": 'pixelSize',
                }
            })

        # В 1 строке заполняем названия залов
        # заливаем ячейки фоном
        for calendar in CALENDAR_LIST:
            self.requests.append({
                "updateCells": {
                    "rows": [
                        {
                            "values": [
                                {
                                    "userEnteredValue": {"stringValue": calendar['name']},
                                    "userEnteredFormat": {
                                        "horizontalAlignment": "CENTER",
                                        "backgroundColor": {
                                            "red": int(calendar['backgroundColor'][0:2], 16) / 255,
                                            "green": int(calendar['backgroundColor'][2:4], 16) / 255,
                                            "blue": int(calendar['backgroundColor'][4:6], 16) / 255,
                                        }
                                    }
                                }
                            ]
                        }
                    ],
                    "fields": "userEnteredValue,userEnteredFormat",
                    "range": {
                        "sheetId": self.sheet_id,
                        "startRowIndex": 0,
                        "endRowIndex": 1,
                        "startColumnIndex": CALENDAR_LIST.index(calendar) + 1,
                        "endColumnIndex": CALENDAR_LIST.index(calendar) + 2
                    }
                }
            })
    
        # Закрепляем первую строку и столбец
        self.requests.append({
            "updateSheetProperties": {
                "properties": {
                    "sheetId": self.sheet_id,
                    "gridProperties": {
                        "frozenRowCount": 1,
                        "frozenColumnCount": 1
                    }
                },
                "fields": "gridProperties.frozenRowCount,gridProperties.frozenColumnCount"
            }
        })
    
    # Заполнение ОДНОГО дня недели
    # Занимает 28 строк!
    def second_setup_sheet(self):
        start_row = 29 # 28 строк + 1 строка с названием дня
        start_col = 1
        day = 2
        day_name = f"{day} {MONTHS[app_state.now.month]}, {get_month_info()['first_weekday']}"
        
        # Объединение ячеек первой строки дня
        self.requests.append({
                "mergeCells": {
                    "range": {
                        "sheetId": self.sheet_id,
                        "startRowIndex": start_row,
                        "endRowIndex": start_row + 1,
                        "startColumnIndex": start_col,
                        "endColumnIndex": start_col + 5
                    },
                    "mergeType": "MERGE_ALL"
                }
            })
            
        # Вставка текста с названием дня недели
        self.requests.append({
            "updateCells": {
                "rows": [
                    {
                        "values": [
                            {
                                "userEnteredValue": {"stringValue": day_name},
                                "userEnteredFormat": {
                                    "horizontalAlignment": "CENTER",
                                    "textFormat": {"bold": True}
                                }
                            }
                        ]
                    }
                ],
                "range": {
                    "sheetId": self.sheet_id,
                    "startRowIndex": start_row,
                    "endRowIndex": start_row + 1,
                    "startColumnIndex": 1,
                    "endColumnIndex": 6
                },
                "fields": "userEnteredValue,userEnteredFormat"
            }
        })

        # Заполнение столбца времени
        for time in TIME_INTERVAL:
            self.requests.append({
                "updateCells": {
                    "rows": [
                        {
                            "values": [
                                {
                                    "userEnteredValue": {"stringValue": time},
                                    "userEnteredFormat": {
                                        "horizontalAlignment": "CENTER",
                                        "textFormat": {"fontSize": 9}
                                    }
                                }
                            ]
                        }
                    ],
                    "start": {
                        "sheetId": self.sheet_id,
                        "rowIndex": start_row + 1 + TIME_INTERVAL.index(time),
                        "columnIndex": 0
                    },
                    "fields": "userEnteredValue,userEnteredFormat"
                }
            })
