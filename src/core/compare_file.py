from pathlib import Path
from core.app_state import app_state
import json

class CompareFiles:  # true / false
    def __init__(self, calendar_data):
        self.logger = app_state.logger
        self.valid = False
        self.data_dir = app_state.data_dir
        self.calendar_alias = calendar_data['alias']
        self.list_files = list(self.data_dir.glob(f"{self.calendar_alias}_*.json"))

        if not self.list_files:
            #self.logger.info(f"Для календаря {self.calendar_alias} не найдено файлов данных.")
            return
        else:
            self.valid = True
            self.latest_young_file = max(self.list_files, key=lambda f: f.stat().st_mtime)
            #self.logger.debug(f"Найден последний файл: {self.latest_young_file.name}")

    def load_sync_token(self, path):
        try:
            with open(path, "r") as f:
                token = json.load(f).get("syncToken")
                #self.logger.debug(f"Загружен syncToken из {path.name}: {token}")
                return token
        except Exception as e:
            self.logger.error(f"Ошибка при загрузке syncToken из {path.name}: {e}")
            return None

    def delete_old_files(self):
        for file in self.list_files:
            try:
                file.unlink()
                #self.logger.debug(f"Удалён устаревший файл: {file.name}")
            except Exception as e:
                self.logger.error(f"Ошибка при удалении {file.name}: {e}")

    def compare_files(self, new_sync_token):
        old_sync_token = self.load_sync_token(self.latest_young_file)

        if old_sync_token == new_sync_token:
            self.logger.info(f"Токены совпадают для {self.calendar_alias}. Синхронизация не требуется.")
            return True
        else:
            self.logger.info(f"Токены различаются для {self.calendar_alias}. Требуется полная синхронизация.")
            app_state.list_changed_calendars.append(self.calendar_alias)
            self.delete_old_files()
            return False
        