from datetime import datetime
from datetime import date
def format_info(event):
    try:
        event.formatted_date = event.date.strftime('%a, %d %B %Y')  
        event.formatted_start = datetime.strptime(event.start_time, '%H:%M').strftime('%I:%M %p') 
        event.formatted_end = datetime.strptime(event.end_time, '%H:%M').strftime('%I:%M %p')  
    except Exception as e:
        print(f"Error formatting event: {e}")
        event.formatted_date = event.date
        event.formatted_start = event.start_time
        event.formatted_end = event.end_time
    return event

