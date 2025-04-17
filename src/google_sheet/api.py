from core.app_state import app_state
from dotenv import load_dotenv
from .utils import MONTHS
from google_sheet.setup_sheet import SetupSheet
import os
import json

load_dotenv()

class SheetAPI:
    def __init__(self):
        self.service = app_state.sheet_service
        self.table_id = os.getenv("TABLE_ID")
        self.requests = []
        
    def list_sheets(self):
        sheets_data = self.service.spreadsheets().get(
            spreadsheetId=self.table_id,
            fields="sheets.properties(sheetId,title)"
        ).execute()["sheets"]

        with open(app_state.sheets_cache_file, "w", encoding="utf-8") as f:
            json.dump(sheets_data, f, ensure_ascii=False, indent=2)
        '''
        {'sheets': 
            ...
            {'properties': {'sheetId': 1165124638, 'title': 'Апрель 2025'}}]}
        '''

    def create_monthly_sheet(self):
        month_name = f"{MONTHS[app_state.now.month]} {app_state.now.year}"

        print('month_name', month_name)
        
        for sheet in app_state.sheets_cache:
            if month_name == sheet['properties']['title']:
                print('exists')
                return

        print('not exists')
        
        # requests = [{
        #     "addSheet": {
        #         "properties": {
        #             "title": month_name
        #         }
        #     }
        # }]

        # self.service.spreadsheets().batchUpdate(
        #     spreadsheetId=self.table_id,
        #     body={"requests": requests}
        # ).execute()
    
    def setup_new_sheet(self):
        pass

    def test_test(self):
        from google_sheet.setup_sheet import SetupSheet
        setup = SetupSheet()
        #setup.first_setup_sheet()
        setup.second_setup_sheet()
        self.service.spreadsheets().batchUpdate(
                    spreadsheetId=self.table_id,
                    #body={"requests": setup.requests_first}
                    body={"requests": setup.requests_second}
                ).execute()
