
from google_calendar.utils import CALENDAR_LIST
from google_sheet.utils import TIME_INTERVAL

class SetupNewSheet:
    def __init__(self, sheet_id):
        self.sheet_id = sheet_id
        self.requests_first = []
        self.requests_second = []

    # Скрываем столбцы !(с 7 по 27 в интерфейсе)
    # Выставляем ширину столбцов
    # Названия в 1 строке
    # Закрепляем и рамка 1 строка и 1 столбец
    def first_setup_sheet(self):
        # скрыть столбцы !(с 7 по 27 в интерфейсе)
        self.requests_first.append({
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
            self.requests_first.append({
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
            self.requests_first.append({
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
        self.requests_first.append({
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

        # Первый столбец фон
        self.requests_first.append({
            "repeatCell": {
                "range": {
                    "sheetId": self.sheet_id,
                    "startColumnIndex": 0, 
                    "endColumnIndex": 1
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColorStyle": {
                            "rgbColor": {
                                "red": int('ff', 16) / 255,
                                "green": int('f2', 16) / 255,
                                "blue": int('cc', 16) / 255,
                            }
                        }
                    }
                },
                "fields": "userEnteredFormat.backgroundColorStyle"
            }
        })
    
        # Рамка первая строка и столбец
        border_style = {
            "style": "SOLID",
            "width": 1,
            "color": {"red": 0, "green": 0, "blue": 0}
        }

        self.requests_first.append({
            "updateBorders": {
                "range": {
                    "sheetId": self.sheet_id,
                    "startRowIndex": 0,
                    "endRowIndex": 1,
                },
                "innerHorizontal": border_style,
                "innerVertical": border_style
            }
        })

        self.requests_first.append({
            "updateBorders": {
                "range": {
                    "sheetId": self.sheet_id,
                    "startColumnIndex": 0,
                    "endColumnIndex": 1
                },
                "bottom": border_style,
                "right": border_style,
                "innerHorizontal": border_style
            }
        })

    # Заполнение ОДНОГО дня недели
    # Занимает всего 31 строку!
    def second_setup_sheet(self, start_row, day_name):
        #start_row 1/31/61
        
        # Объединение ячеек первой строки дня и рамка
        border_style = {
            "style": "SOLID",
            "width": 1,
            "color": {"red": 0, "green": 0, "blue": 0}
        }

        self.requests_second.append({
            "mergeCells": {
                "range": {
                    "sheetId": self.sheet_id,
                    "startRowIndex": start_row,
                    "endRowIndex": start_row + 1,
                    "startColumnIndex": 1,
                    "endColumnIndex": 6
                },
                "mergeType": "MERGE_ALL"
            }
        })
        self.requests_second.append({
            "updateBorders": {
                "range": {
                    "sheetId": self.sheet_id,
                    "startRowIndex": start_row,
                    "endRowIndex": start_row + 1,
                    "startColumnIndex": 1,
                    "endColumnIndex": 6
                },
                "top": border_style,
                "bottom": border_style,
                "left": border_style,
                "right": border_style
            }
        })

        # Правая рамка в последнем столбце
        self.requests_second.append({
            "updateBorders": {
                "range": {
                    "sheetId": self.sheet_id,
                    "startColumnIndex": 5,
                    "endColumnIndex": 6
                },
                "right": border_style
            }
        })

        # Вставка текста с названием дня недели
        self.requests_second.append({
            "repeatCell": {
                "range": {
                    "sheetId": self.sheet_id,
                    "startRowIndex": start_row,
                    "endRowIndex": start_row + 1,
                    "startColumnIndex": 1,
                    "endColumnIndex": 6
                },
                "cell": {
                    "userEnteredValue": {"stringValue": day_name},
                    "userEnteredFormat": {
                        "horizontalAlignment": "CENTER",
                        "textFormat": {"bold": True}
                    }
                },
                "fields": "userEnteredValue,userEnteredFormat(horizontalAlignment,textFormat)"
            }
        })

        # Заполнение столбца времени
        for time in TIME_INTERVAL:
            self.requests_second.append({
                "repeatCell": {
                    "range": {
                        "sheetId": self.sheet_id,
                        "startRowIndex": start_row + 1 + TIME_INTERVAL.index(time),
                        "endRowIndex": start_row + 2 + TIME_INTERVAL.index(time),
                        "startColumnIndex": 0,
                        "endColumnIndex": 1
                    },
                    "cell": {
                        "userEnteredValue": {"stringValue": time},
                        "userEnteredFormat": {
                            "horizontalAlignment": "CENTER",
                            "textFormat": {
                                "fontSize": 9
                            }
                        }
                    },
                    "fields": "userEnteredValue,userEnteredFormat(textFormat,horizontalAlignment)"
                }
            })
