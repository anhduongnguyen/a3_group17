from flask import Blueprint, render_template, request, flash, redirect, url_for
from .forms import EventForm
from .models import Event, CreateEvent
from . import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Fetch all events from the CreateEvent table
    events = CreateEvent.query.order_by(CreateEvent.date).all()
    return render_template('index.html', events=events)

@main_bp.route('/create-event', methods=['GET', 'POST'])
def create_event():
    form = EventForm()
    if form.validate_on_submit(): 
        new_event = CreateEvent(
            title=form.event_name.data,
            description=form.description.data,
            date=form.event_date.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            cuisine=form.cuisine_type.data,
            tickets=form.tickets.data,
            location=form.location.data,
            image=form.image.data.filename if form.image.data else None
        )

        
        db.session.add(new_event)
        db.session.commit()
        #put u back on the home page to see the new event 
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