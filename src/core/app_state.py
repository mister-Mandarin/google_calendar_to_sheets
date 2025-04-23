from dataclasses import dataclass, field
from typing import Any
from datetime import datetime
from core.auth import Auth
from pathlib import Path
from core.logger import AppLogger
import json

@dataclass
class AppState:
    now: str = datetime.now()
    sheet_service: Any = field(init=False)
    calendar_service: Any = field(init=False)
    sheets_cache: Any = field(init=False)
    sheets_cache_file: str = "cached_sheets.json"
    data_dir: Path = Path(__file__).parent.parent.parent / 'data'
    list_changed_calendars: Any = field(default_factory=list)
    logger: Any = field(init=False)

    def __post_init__(self):
        self._init_services()
        self._init_data_dir()
        self._load_sheets_cache()
        self.logger = AppLogger(name="app", log_dir=self.data_dir).get_logger()
        self.logger.info("__________________________________________________________")
        self.logger.debug(f"Запуск {self.now}.")

    def _init_services(self):
        auth = Auth()
        self.sheet_service = auth.get_service("table")
        self.calendar_service = auth.get_service("calendar")
    
    def _init_data_dir(self):
        self.data_dir.mkdir(exist_ok=True)

    def _load_sheets_cache(self):
        try:
            with open(self.data_dir / self.sheets_cache_file, "r", encoding="utf-8") as f:
                self.sheets_cache = json.load(f)
        except FileNotFoundError:
            self.sheets_cache = []

    def _save_sheets_cache(self, sheets_cache):
        try:
            with open(self.data_dir / self.sheets_cache_file, "w", encoding="utf-8") as f:
                json.dump(sheets_cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.error(f"Ошибка при сохранении sheets_cache: {e}")
        
        self._load_sheets_cache()

# Инициализируем глобальный экземпляр
app_state = AppState()