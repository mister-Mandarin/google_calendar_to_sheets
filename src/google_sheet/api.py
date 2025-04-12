from core.app_state import app_state
from dotenv import load_dotenv
from .utils import MONTHS
import os

load_dotenv()

class SheetAPI:
    def __init__(self):
        self.service = app_state.sheet_service
        self.table_id = os.getenv("TABLE_ID")
        
    def list_sheets(self):
        spreadsheet = self.service.spreadsheets().get(
            spreadsheetId=self.table_id,
            fields="sheets.properties(sheetId,title)"
        ).execute()
        '''
        {'sheets': 
            ...
            {'properties': {'sheetId': 1165124638, 'title': 'Апрель 2025'}}]}
        '''
    
        return spreadsheet

    def create_monthly_sheet(self):
        month_name = f"{MONTHS[app_state.now.month]} {app_state.now.year}"

        if month_name in self.list_sheets():
            return
        
        body = {
            "requests": [{
                "addSheet": {
                    "properties": {
                        "title": month_name
                    }
                }
            }]
        }

        self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.table_id,
            body=body
        ).execute()
    
    def setup_new_sheet(self):
        pass

    def create_day_month(self):
        pass

    def test_test(self):
        from google_sheet.setup_sheet import SetupSheet
        setup = SetupSheet()
        #setup.first_setup_sheet()
        setup.second_setup_sheet()
        self.service.spreadsheets().batchUpdate(
                    spreadsheetId=self.table_id,
                    body={"requests": setup.requests}
                ).execute()
