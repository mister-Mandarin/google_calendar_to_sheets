from datetime import time, datetime
from core.utils import stable_hash
from core.app_state import app_state

def format_event(raw_events):
    #app_state.logger.debug("raw_events: " + str(raw_events))

    events_items = raw_events.get("items", [])
    processed_events = {
        "syncToken": stable_hash(raw_events.get("updated")),
        "items": []
    }

    # Преобразуем события в объекты datetime
    events = []
    for event in events_items:
        try:
            start = datetime.fromisoformat(event["start"]["dateTime"])
            end = datetime.fromisoformat(event["end"]["dateTime"])
            events.append({
                "id": event["id"],
                "start": start,
                "end": end
            })
        except KeyError as e:
            app_state.logger.error(f"Ошибка при обработке события: {e}. Событие: {event}")
            continue

    # Группируем по дням пересекающиеся события в один день
    grouped_events = {}
    for event in events:
        day_key = event["start"].date()
        if day_key not in grouped_events:
            grouped_events[day_key] = []
        grouped_events[day_key].append(event)

    #app_state.logger.debug("grouped_events: " + str(grouped_events))

    # Объединяем пересекающиеся события в каждой группе
    # Берем граничные состояния пересекающихся событий
    merged_events = []
    for day, day_events in grouped_events.items():
        if not day_events:
            continue
            
        current_event = day_events[0].copy()

        for event in day_events[1:]:
            if event["start"] < current_event["end"]:
                # Объединяем события
                current_event["end"] = max(current_event["end"], event["end"])
            else:
                # Добавляем текущее объединенное событие и начинаем новое
                merged_events.append(current_event)
                current_event = event.copy()
        
        merged_events.append(current_event)

    nine_am = time(9, 0, 0)
    twenty_three_pm = time(23, 0, 0)

    # # Конвертируем обратно в строки
    for event in merged_events:
        start_dt = event["start"]
        end_dt = event["end"]

        # Проверка времени начала и конца
        if start_dt.time() < nine_am:
            if end_dt.time() <= nine_am:
                # Начало и конец раньше 9:00, игнорируем событие
                continue
            else:
                # Начало раньше 9:00, конец позже
                # Устанавливаем начало на 9:00 того же дня
                start_dt = datetime.combine(start_dt.date(), nine_am, tzinfo=start_dt.tzinfo)

        # Конец позже 22:00 или на следующий день
        if end_dt.time() > twenty_three_pm or end_dt.date() > start_dt.date():
            end_dt = datetime.combine(start_dt.date(), twenty_three_pm, tzinfo=end_dt.tzinfo)      

        start = start_dt.isoformat()
        end = end_dt.isoformat()

        processed_events["items"].append({
            "id": event["id"],
            "start": start,
            "end": end
        })
    
    return processed_events