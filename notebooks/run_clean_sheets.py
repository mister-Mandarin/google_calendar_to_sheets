from google_sheet.check_sheet_id import CheckSheetId 
from google_sheet.clean_sheet import CleanSheet
from core.app_state import app_state
from itertools import pairwise

# Пример состояния    
# list_changed_calendars = ['big120', 'big90', 'medium60', 'small16']

def get_id_from_cache(data):
  """Получить данные листа из кэша"""
  if data[:7] in app_state.sheets_cache:
    return app_state.sheets_cache[data[:7]]

def get_id_table(sheet_dates_ragne, alias):
  """
  Перебрать даты списка.
  Подготовить запрос на очистку по датам.
  Отправить запрос.
  """
  clean = CleanSheet(alias)

  for start_cleaning_date, end_cleaning_date in pairwise(sheet_dates_ragne):
    
    table_data_cache = get_id_from_cache(start_cleaning_date)
    
    clean.clean_until(start_cleaning_date, end_cleaning_date, table_data_cache['sheetId'])

def run_clean_sheet():
  for alias in app_state.list_changed_calendars:
    # Загрузка данных, поиск/создание id листов
    setup = CheckSheetId(alias)
    setup.check_sheets_id()
    get_id_table(setup.sheet_dates_ragne, alias)
