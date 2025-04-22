import sys
from pathlib import Path 

sys.path.append(str(Path.cwd().parent / 'src'))
from google_calendar.api import CalendarAPI
from google_calendar.utils import CALENDAR_LIST

def run_calendar_operations():
    for calendar_data in CALENDAR_LIST:
        calendar = CalendarAPI(calendar_data)
        if not calendar.exists_calendar():
            calendar.add_calendar()
        calendar.get_events()

# # Настройки повторов
# RETRY_SETTINGS = {
#     'stop': stop_after_attempt(5),
#     'wait': wait_exponential(multiplier=1, min=2, max=30),
#     'retry': retry_if_exception_type((HttpError, TimeoutError)),
#     'before_sleep': before_sleep_log(app_state.logger, logging.WARNING),
#     'before': before_log(app_state.logger, logging.INFO),
#     'after': after_log(app_state.logger, logging.INFO)
# }

# loop = asyncio.get_running_loop()

# @retry(**RETRY_SETTINGS)
# async def process_calendar(calendar_data):
#     try:
#         app_state.logger.info(f"▶ Начало обработки: {calendar_data['alias']}")
#         calendar_api = CalendarAPI(calendar_data.copy())
        
#         exists = await loop.run_in_executor(None, calendar_api.exists_calendar)
        
#         if not exists:
#             await loop.run_in_executor(None, calendar_api.add_calendar)
        
#         await loop.run_in_executor(None, calendar_api.get_events)
        
#     except HttpError as e:
#         app_state.logger.error(f"Google API Error: {e}")
#         raise
#     except Exception as e:
#         app_state.logger.error(f"Неизвестная ошибка: {str(e)}")
#         raise

# async def main():
#     app_state.logger.info("⏳ Запуск параллельной обработки календарей...")
    
#     # Ограничиваем параллелизм для избежания Rate Limits
#     semaphore = asyncio.Semaphore(2)
    
#     async def limited_task(calendar):
#         async with semaphore:
#             return await process_calendar(calendar)
    
#     tasks = [limited_task(calendar) for calendar in CALENDAR_LIST]
#     await asyncio.gather(*tasks, return_exceptions=True)
    
#     app_state.logger.info("🏁 Обработка всех календарей завершена.")

# def run_calendar_operations():
#     try:
#         # Для Jupyter/существующего цикла
#         return loop.create_task(main())
#     except RuntimeError:
#         # Для production/скриптов
#         return asyncio.run(main())