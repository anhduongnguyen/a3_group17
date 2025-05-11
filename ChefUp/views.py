from datetime import datetime
from flask import Blueprint, current_app, render_template, request, flash, redirect, url_for
from .forms import EventForm
from . import db
import os
from werkzeug.utils import secure_filename
from .models import Event, Booking, Comment


main_bp = Blueprint('main', __name__)



@main_bp.route('/')
def index():
    events = Event.query.order_by(Event.date).all()
    for event in events:
        try:
            event.formatted_start = datetime.strptime(event.start_time, '%H:%M').strftime('%I:%M %p')
            event.formatted_end = datetime.strptime(event.end_time, '%H:%M').strftime('%I:%M %p')
            event.formatted_date = event.date.strftime('%d %b %Y') 
        except Exception:
            event.formatted_start = event.start_time
            event.formatted_end = event.end_time
            event.formatted_date = event.date
    return render_template('index.html', events=events)

## will need to move event related stuff to its own file to be neater
@main_bp.route('/create-event', methods=['GET', 'POST'])
def create_event():
    test_user_id = 1
    form = EventForm()
    if form.validate_on_submit(): 
        image_path = check_upload_file(form)

        new_event = Event(
            title=form.event_name.data,
            description=form.description.data,
            date=form.event_date.data,
            start_time=form.start_time.data.strftime('%H:%M'),
            end_time=form.end_time.data.strftime('%H:%M'),
            location=form.location.data,
            price=form.price.data,
            capacity=form.tickets.data,
            image_filename=image_path,
            user_id=test_user_id,
            status='Open'
        )

        db.session.add(new_event)
        db.session.commit()
        flash("Event created successfully!", "success")
        return redirect(url_for('main.index'))

    return render_template('create-event.html', form=form)

@main_bp.route('/booking-history')
def booking_history():
    return render_template('booking-history.html')

@main_bp.route('/event-detail')
def event_detail(event_id):
    return render_template('event-detail.html')

@main_bp.route('/error')
def error():
    return render_template('error.html')

@main_bp.route('/book-event')
def book_event(event_id):
    return render_template('book-event.html')

def check_upload_file(form):
    file = form.image.data
    if not file:
        return None
    filename = secure_filename(file.filename)
    upload_path = os.path.join(current_app.root_path, 'static', 'uploaded_img', filename)
    os.makedirs(os.path.dirname(upload_path), exist_ok=True)
    file.save(upload_path)
    return f'uploaded_img/{filename}'

'''
@main_bp.route('/event-detail/<int:event_id>')
def event_detail(event_id):
    # Optional: fetch event from database using event_id
    return render_template('event-detail.html', event_id=event_id)
    
@main_bp.route('/book-event/<int:event_id>', methods=['POST'])
@login_required
def book_event(event_id):
    # Add booking logic here (e.g., create Booking instance)
    # Example:
    # quantity = int(request.form['quantity'])
    # create booking record in DB
    flash('Successfully booked the event!', 'success')
    return redirect(url_for('main.booking_history'))
'''