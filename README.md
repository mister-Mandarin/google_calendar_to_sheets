## Google Calendar to Google Sheets

!!!Python 3.10.7 or greater

### Helpers
```bash
pip freeze > requirements.txt # добавить пакеты в файл
```

```bash
google_calendar_to_sheets/
│
├── data/                         # Создается при первом запуске  
│   ├── app.log                      # Лог программы 
│   ├── big90_2025-04-26_14-12.json  # Пример файла с данными
│   └── cached_sheets.json           # Словарь с данными существующих календарей
│
├── notebooks/             # Главные исполняемые файлы
│   ├── main.py               # Основной скрипт
│   ├── run_calendar.py       # Получение/проверка/анализ/запись данных календарей
│   ├── run_clean_sheets.py   # Очистка записанных данных/создание и насторйка листов/создание cached_sheets.json 
│   └── run_write_sheets.py   # Запись данных измененных календарей
│
├── src/
│   │
│   ├── core/               # Общая логика
│   │   ├── app_state.py       # Глобальное состояние программы
│   │   ├── auth.py            # Аутентификация
│   │   ├── create_file.py     # Создание файлов
│   │   ├── credentials.json   # Файл сервисного аккаунта (добавить)
│   │   ├── logger.py          # Логирование ошибок
│   │   └── utils.py           # Вспомогательные функции  
│   │
│   ├── google_calendar/    # Логика работы с Google Calendar
│   │   ├── api.py             # Работа с Calendar API
│   │   ├── compare_file.py    # Сравнение файлов
│   │   ├── formatter.py       # Форматирование данных/испавление ошибок
│   │   └── utils.py           # Вспомогательные функции
│   │
│   └── google_sheets/      # Логика работы с Google Sheets
│       ├── api.py             # Проверка и создание листов
│       ├── check_sheets.py    # Поиск id листа для записи данных по дате
│       ├── clean_sheet.py     # Очистка листа
│       ├── config_sheet.py    # Общий класс с методами и константами для работы с листом
│       ├── setup_new_sheet.py # Настройка и заполнение нового листа
│       ├── utils.py           # Вспомогательные функции
│       └── write_event.py     # Запись данных в лист
│
├── .env                       # Переменные окружения (добавить)
├── .gitignore                # Игнорируемые файлы
├── README.md                 # Описание
└── requirements.txt          # Зависимости Python

```
### Help links auth
https://developers.google.com/workspace/calendar/api/quickstart/python

### Help links calendar
https://developers.google.com/workspace/calendar/api/v3/reference/events/list 
https://developers.google.com/workspace/calendar/api/guides/sync 
https://developers.google.com/workspace/calendar/api/guides/performance 

### Help links sheets
https://developers.google.com/workspace/sheets/api/reference/rest
https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/batchUpdate 

## Bugs/features
Не создается при первом запуске файл cached_sheets.json
+ Добавить логи при добавлении/очистке и записи календарей
+ Падает check_sheet_id.py", line 36, in get_range_dates raise ValueError("Список items пуст.")
