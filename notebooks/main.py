from sys import path
from pathlib import Path
from locale import setlocale, LC_ALL 

#path.append(str(Path.cwd().parent / 'src')) 
path.append(str(Path(__file__).parent.parent / "src"))
from core.app_state import app_state 
  
setlocale(LC_ALL, 'ru_RU.UTF-8')

from run_calendar import run_calendar_operations 
from run_clean_sheets import run_clean_sheet
from run_write_sheets import run_write_sheets

run_calendar_operations()
run_clean_sheet()
run_write_sheets()
 
print('done') 
 