from datetime import datetime
from datetime import date

def format_info(event):
    event.formatted_date = event.date.strftime('%a, %d %B %Y')
    event.formatted_start = event.start_time.strftime('%I:%M %p')  
    event.formatted_end = event.end_time.strftime('%I:%M %p')  

    return event

def status_badge_class(status):
    status = status.lower()
    if status == "cancelled":
        return "danger"
    elif status == "sold out":
        return "secondary"
    elif status == "past":
        return "secondary"
    elif status == "open":
        return "success"
    else:
        return "info" 
    

def validate_times(event_date, start_time, end_time):
    errors = []

    if end_time <= start_time:
        errors.append("End time must be after start time.")

    start_datetime = datetime.combine(event_date, start_time)
    if start_datetime < datetime.now():
        errors.append("Start time cannot be in the past.")

    return errors

