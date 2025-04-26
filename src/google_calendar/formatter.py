from datetime import datetime
from core.utils import stable_hash

def format_event(raw_events):
    events_items = raw_events.get("items", [])
    processed_events = {
        "syncToken": stable_hash(raw_events.get("updated")),
        "items": []
    }

    # Преобразуем события в объекты datetime и сортируем
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
        except KeyError:
            continue
    
    # Сортируем события по времени начала
    events.sort(key=lambda x: x["start"])

    # Группируем по дням
    grouped_events = {}
    for event in events:
        day_key = event["start"].date()
        if day_key not in grouped_events:
            grouped_events[day_key] = []
        grouped_events[day_key].append(event)

    # Объединяем пересекающиеся события в каждой группе
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

    # Конвертируем обратно в строки
    for event in merged_events:
        processed_events["items"].append({
            "id": event["id"],
            "start": event["start"].isoformat(),
            "end": event["end"].isoformat()
        })

    return processed_events