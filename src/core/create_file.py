import json
from pathlib import Path
from google_calendar.formatter import format_event

class File:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent.parent / 'data'
        self.data_dir.mkdir(exist_ok=True)

    def write_file(self, calendar_data, events, date_file):
        file_name = f"{calendar_data["alias"]}_{date_file}.json"

        with open(self.data_dir / file_name, 'w') as file:
            json.dump(format_event(events), file, indent=2)
            
            #json.dump(events, file, indent=2)