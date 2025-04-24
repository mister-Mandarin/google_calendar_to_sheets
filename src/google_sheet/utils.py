MONTHS_DAYS = ['', 'Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня', 'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря']

MONTHS = ['','Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

TIME_INTERVAL = [f"{hour:02d}:{minute:02d}" for hour in range(9, 24) for minute in (0, 30) if not (hour == 23 and minute == 30)]

WEEKDAYS = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']

import calendar
from google_calendar.utils import CALENDAR_LIST
from datetime import datetime
from dateutil import parser
 
def get_month_info(month: str):

    month_name, year = month.split("_")
    month_index = MONTHS.index(month_name)
    year = int(year)

    first_weekday_number, total_days = calendar.monthrange(year, month_index)
    
    return first_weekday_number, total_days

def get_count_days(start_day, end_day):
    """Возвращает разницу в днях между датами с учётом временной зоны."""
    # Парсим даты с временными зонами
    start = parser.isoparse(start_day)
    end = parser.isoparse(end_day)
    
    return (end.date() - start.date()).days


def get_index_column_by_alias(alias):
   """
   Возвращает координату начала и конца столбца
   """
   for i, cal in enumerate(CALENDAR_LIST):
    if cal['alias'] == alias:
        return i + 1, i + 2