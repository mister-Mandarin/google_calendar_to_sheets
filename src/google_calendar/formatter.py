def format_event(raw_events):
    events_items = raw_events.get("items", [])
    events = {
        "syncToken": hash(raw_events.get("updated")),
        "items": []
    }

    for event in events_items:
        events["items"].append({
            "id": event["id"],
            "start": event["start"]["dateTime"], 
            "end": event["end"]["dateTime"],
        })

    return events
  