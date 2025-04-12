MONTHS = {
    1: "Января",
    2: "Февраля",
    3: "Марта",
    4: "Апреля",
    5: "Мая",
    6: "Июня",
    7: "Июля",
    8: "Августа",
    9: "Сентября",
    10: "Октября",
    11: "Ноября",
    12: "Декабря"
}

TIME_INTERVAL = [f"{hour:02d}:{minute:02d}" for hour in range(10, 24) for minute in (0, 30) if not (hour == 23 and minute == 30)]

WEEKDAYS = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']

def get_month_info():
    import calendar
    from core.app_state import app_state

    first_weekday, total_days = calendar.monthrange(app_state.now.year, app_state.now.month)
    return {
        "first_weekday": WEEKDAYS[first_weekday],
        "total_days": total_days
    }