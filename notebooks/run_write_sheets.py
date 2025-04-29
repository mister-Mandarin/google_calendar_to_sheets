from google_sheet.write_event import WriteEvent
from core.app_state import app_state

# Пример состояния    
#list_changed_calendars = ['big90', 'medium60', 'small16']
def run_write_sheets():
    for sheet in app_state.list_changed_calendars:
        app_state.logger.info(f"Перезаписываю календарь {sheet}")
        items = WriteEvent(sheet)
        items.write_event_block()