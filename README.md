

### Helpers
```bash
pip freeze > requirements.txt # добавить пакеты в файл
```

```bash
google_calendar_to_sheets/
│
├── data/                     # Создается при первом запуске, json-ы c данными   
│
├── notebooks/
│   └── main.ipynb            # Основной скрипт (точка входа)
│
├── src/
│   │
│   ├── google_calendar/      # Логика работы с Google Calendar
│   │   ├── api.py            # Запросы к Calendar API
│   │   └── parser.py         # Преобразование данных
│   │
│   ├── sheets/               # Логика работы с Google Sheets
│   │   ├── api.py            # Запросы к Sheets API
│   │   └── formatter.py      # Форматирование таблицы
│   │
│   └── core/                 # Общая логика
│       ├── auth.py
│       ├── logger.py         # Логирование ошибок
│       ├── utils.py
│       └── credentials.json  # Файл сервисного аккаунта (добавить)
│
├── .github/                  # GitHub Actions
│   └── workflows/
│       └── scheduler.yml     # Расписание запусков
│
├── .env
├── requirements.txt          # Зависимости Python
├── .gitignore
└── README.md

```