import json
from pathlib import Path
from google_calendar.formatter import format_event
from core.app_state import app_state

class File:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent.parent / 'data'

    def write_file(self, calendar_data, events):
        file_name = f"{calendar_data["alias"]}_{app_state.now.strftime("%Y-%m-%d_%H-%M")}.json"

        with open(self.data_dir / file_name, 'w') as file:
            json.dump(format_event(events), file, indent=2)