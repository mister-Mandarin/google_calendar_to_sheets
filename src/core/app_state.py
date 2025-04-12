from dataclasses import dataclass, field
from typing import Any
from datetime import datetime
from core.auth import Auth

@dataclass
class AppState:
    now: str = datetime.now()
    sheet_service: Any = field(init=False)
    calendar_service: Any = field(init=False)

    def __post_init__(self):
        auth = Auth()
        self.sheet_service = auth.get_service("table")
        self.calendar_service = auth.get_service("calendar")
    
# Инициализируем глобальный экземпляр
app_state = AppState()