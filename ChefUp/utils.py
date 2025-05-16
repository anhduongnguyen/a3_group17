from datetime import datetime

def format_info(event):
    try:
        # Format date
        event.formatted_date = event.date.strftime('%a, %d %B %Y')  # Example: Thursday, 15 May 2025
        # Format time
        event.formatted_start = datetime.strptime(event.start_time, '%H:%M').strftime('%I:%M %p')  # Example: 02:30 PM
        event.formatted_end = datetime.strptime(event.end_time, '%H:%M').strftime('%I:%M %p')  # Example: 04:00 PM
    except Exception as e:
        print(f"Error formatting event: {e}")
        event.formatted_date = event.date
        event.formatted_start = event.start_time
        event.formatted_end = event.end_time
    return event