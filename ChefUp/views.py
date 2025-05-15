from datetime import datetime
from flask import Blueprint, current_app, render_template, request, flash, redirect, url_for
from flask import abort
from .forms import EventForm
from . import db
import os
from werkzeug.utils import secure_filename
from .models import Event, Booking, Comment
from datetime import date
from .utils import format_info


main_bp = Blueprint('main', __name__)

event_bp = Blueprint('events', __name__, url_prefix='/events') 

@main_bp.route('/')
def index():
    events = Event.query.order_by(Event.date).all()
    for event in events:
        format_info(event)  
    return render_template('index.html', events=events)

@event_bp.route('/create-event', methods=['GET', 'POST'])
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
            cuisine=form.cuisine.data,
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
    

    return render_template('create-event.html', form=form, current_date=date.today().strftime('%Y-%m-%d'))

@main_bp.route('/booking-history')
def booking_history():
    return render_template('booking-history.html')

@event_bp.route('/<int:event_id>')
def event_detail(event_id):
    event = db.session.get(Event, event_id)
    if event is None:
        abort(404)
    
    format_info(event)  
    
    return render_template('event-detail.html', event=event)

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

@main_bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error_code="404 - Page Not Found", 
                           message="The link you followed is broken or the page has been removed."), 404

@main_bp.app_errorhandler(500)
def internal_server_error(error):
    return render_template('error.html', error_code="500 - Internal Server Error", 
                           message="Something went wrong on our end. Please try again later."), 500

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