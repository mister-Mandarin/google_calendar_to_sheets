from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

class Auth:
    SCOPES = [
        "https://www.googleapis.com/auth/calendar",
        "https://www.googleapis.com/auth/spreadsheets"
    ]
    FILE_PATH = os.path.join(os.path.dirname(__file__), "credentials.json")

    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(
            filename=self.FILE_PATH,
            scopes=self.SCOPES
        )
        self.services = {
            "calendar": build("calendar", "v3", credentials=credentials),
            "sheets": build("sheets", "v4", credentials=credentials)
        }

    def get_service(self, name):
        return self.services.get(name)