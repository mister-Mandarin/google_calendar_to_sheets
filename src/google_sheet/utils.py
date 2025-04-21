MONTHS_DAYS = ['', 'Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня', 'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря']

MONTHS = ['','Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

TIME_INTERVAL = [f"{hour:02d}:{minute:02d}" for hour in range(9, 24) for minute in (0, 30) if not (hour == 23 and minute == 30)]

WEEKDAYS = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']

def get_month_info(month: str):
    import calendar

    month_name, year = month.split("_")
    month_index = MONTHS.index(month_name)
    year = int(year)

    first_weekday_number, total_days = calendar.monthrange(year, month_index)
    
    return first_weekday_number, total_days