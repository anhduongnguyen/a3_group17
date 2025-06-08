from datetime import datetime
from datetime import date
import os
from werkzeug.utils import secure_filename
from flask import current_app

# Format date and time fields for display in templates
def format_info(event):
    event.formatted_date = event.date.strftime('%a, %d %B %Y')
    event.formatted_start = event.start_time.strftime('%I:%M %p')  
    event.formatted_end = event.end_time.strftime('%I:%M %p')  

    return event

# Return a Bootstrap badge class based on event status
def status_badge_class(status):
    status = status.lower()
    if status == "cancelled":
        return "danger"
    elif status == "sold out":
        return "warning"
    elif status == "inactive":
        return "secondary"
    elif status == "open":
        return "success"
    else:
        return "info" 
    

# Validate event date and time fields 
# (event times must be in the future and end time must be after start time)
def validate_times(event_date, start_time, end_time):
    errors = []

    if end_time <= start_time:
        errors.append("End time must be after start time.")

    start_datetime = datetime.combine(event_date, start_time)
    if start_datetime < datetime.now():
        errors.append("Start time cannot be in the past.")

    return errors

# Handles file upload securely and stores the image in the static folder
def check_upload_file(form):
    file = form.image.data
    if not file:
        return None
    
    filename = secure_filename(file.filename)
    upload_path = os.path.join(current_app.root_path, 'static', 'uploaded_img', filename)
    os.makedirs(os.path.dirname(upload_path), exist_ok=True)
    file.save(upload_path)
    return f'uploaded_img/{filename}'
