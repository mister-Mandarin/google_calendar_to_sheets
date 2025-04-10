from pathlib import Path
import json
from datetime import datetime

class CompareFiles: #true / false
    def __init__(self, calendar_data):
        self.valid = False
        self.data_dir = Path(__file__).parent.parent.parent / 'data'
        self.calendar_alias = calendar_data['alias']
        self.list_files = list(self.data_dir.glob(f"{self.calendar_alias}_*.json"))
        if not self.list_files:
            return
        else:
            self.valid = True
            self.latest_young_file = max(self.list_files, key=lambda f: f.stat().st_mtime)

    def load_sync_token(self, path):
        with open(path, "r") as f:
            return json.load(f).get("syncToken")

    def delete_old_files(self, path):
        for file in self.list_files:
            if file != path:
                try:
                    file.unlink()
                except Exception as e:
                    print(f"Ошибка при удалении {file.name}: {e}")

    def compare_files(self, new_sync_token):
        
        self.delete_old_files(self.latest_young_file)
        old_sync_token = self.load_sync_token(self.latest_young_file)
        
        if old_sync_token == new_sync_token:
            return True
        else:
            return False
