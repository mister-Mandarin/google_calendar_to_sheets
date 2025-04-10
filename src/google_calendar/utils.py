import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

CALENDAR_LIST = [
    {
        "id": os.getenv("BIG120"),
        "summary": "Зал 120 кв.м. Центр Альфа-Зет м. Достоевская",
        "alias": 'big120'
    },
]

def get_datetime():
    now = datetime.now()

    time_min = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + "Z"

    if now.month + 2 > 12:
        next_month = now.replace(year=now.year + 1, month=(now.month + 2) % 12, day=1)
    else:
        next_month = now.replace(month=now.month + 2, day=1)

    # Корректировка для февраля и месяцев с <31 днями
    last_day_of_month = (next_month - timedelta(days=1)).day
    time_max = now.replace(
        year=next_month.year,
        month=next_month.month,
        day=min(now.day, last_day_of_month),
        hour=0, minute=0, second=0, microsecond=0
    ).isoformat() + "Z"

    date_file = now.strftime("%Y-%m-%d_%H-%M")

    return date_file, time_min, time_max