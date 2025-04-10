from dataclasses import dataclass, field
from typing import Any
from datetime import datetime
from core.auth import Auth

@dataclass(frozen=True)
class AppState:
    now: str = datetime.now()
    sheets_service: Any
    calendar_service: Any

    def __post_init__(self):
        auth = Auth()
        self.sheets_service = auth.get_service("sheets")
        self.calendar_service = auth.get_service("calendar")
    
# Инициализируем глобальный экземпляр
app_state = AppState()