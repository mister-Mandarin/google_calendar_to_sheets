import os
from dotenv import load_dotenv
from datetime import timedelta
from core.app_state import app_state

load_dotenv()

CALENDAR_LIST = [
    {
        "id": os.getenv("BIG120"),
        "name": "Зал 120/Классика",
        "summary": "Зал 120 кв.м. Центр Альфа-Зет м. Достоевская",
        "alias": 'big120',
        "backgroundColor": "a4c2f4", # "3F51B5" черника/синий
        "colorList": ["A4C2F4", "BCD3FA", "CDDDFA", "355C9F", "8A9BB7"]
    },
    {
        "id": os.getenv("BIG90"),
        "name": "Зал 90/Эзотерика",
        "summary": "Зал в эзотерическом стиле со статуей медитируюшего Будды и возможностью цветного освещения.",
        "alias": 'big90',
        "backgroundColor": "b4a7d6", # "039BE5" павлин/голубой
        "colorList": ["B4A7D6", "C4A2D3", "CFC4EB", "DDC0E9", "E0CBE9"]
    },
        {
        "id": os.getenv("MEDIUM60"),
        "name": "Зал 60/Романтика",
        "summary": "Прямоугольный зал с фантазийными элементами в оформлении.",
        "alias": 'medium60',
        "backgroundColor": "ea9999", # "D50000" помидор/красный
        "colorList": ["EA9999", "F4B5B5", "F4C6C6", "B08282", "DDB3CB"]
    },
    {
        "id": os.getenv("SMALL30"),
        "name": "Малый зал 30/Практика",
        "summary": "Небольшой зал для мини-групп и индивидуальных сессий.",
        "alias": 'small30',
        "backgroundColor": "b6d7a8", # "7CB342" фисташка/зеленый
        "colorList": ["B6D7A8", "D0EBC4", "8FA187", "EFF6D9", "D7EBCF"]
    },
    {
        "id": os.getenv("SMALL16"),
        "name": "Кабинет 16/Массаж",
        "summary": "С кушеткой и местом для беседы с клиентом.",
        "alias": 'small16',
        "backgroundColor": "ffe599", # "F6BF26" банан/желтый
        "colorList": ["FFE599", "FFEBB3", "FFF1C7", "BFBA86", "FFF0C6"]
    }
]

def get_datetime():
    now = app_state.now

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

    return time_min, time_max