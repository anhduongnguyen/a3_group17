from datetime import datetime
from flask import Blueprint, current_app, render_template, request, flash, redirect, url_for, abort
from flask import abort
from flask_login import current_user, login_required
from .forms import CommentingForm, EditEventForm, CreateEventForm, BookingForm
from . import db
import os
from werkzeug.utils import secure_filename
from .models import Event, Booking, Comment, User
from datetime import date
from .utils import format_info, validate_times

# Cuisine filter options for home/index page dropdown
options = [
    'Italian', 'Japanese', 'Mexican',
    'Korean', 'Vietnamese', 'Thai',
    'Indian', 'Chinese', 'French',
    'Spanish', 'Greek', 'Caribbean',
    'Other'
]

# Create blueprint for main routes
main_bp = Blueprint('main', __name__)

#  Route for the home page shows all open or sold-out events, 
# with optional cuisine filtering
@main_bp.route('/')
def index():
    selected_option = request.args.get("options")
    events = Event.query.order_by(Event.date.asc()).all()

    open_events = []
    for event in events:
        if event.update_event_status in ["Open", "Sold Out"]:
            format_info(event)
            if not selected_option or event.cuisine == selected_option:
                open_events.append(event)

    return render_template('index.html', events=open_events, options=options, selected_option=selected_option)

# Route for the user's booking history page (shows both booked and created events)
@main_bp.route('/booking-history')
@login_required
def booking_history():
    now = datetime.now()

    # Booked events by the user
    bookings = (
        Booking.query.filter_by(user_id=current_user.id)
        .join(Event)
        .add_entity(Event)
        .order_by(Event.date.desc())
        .all()
    )

    upcoming_booked = []
    inactive_booked = []

    for booking, event in bookings:
        format_info(event)
        event_end = datetime.combine(event.date, event.end_time)
        booking_info = {
            "title": event.title,
            "cuisine": event.cuisine,
            "image": event.image_filename,
            "update_event_status": event.update_event_status,
            "date": event.formatted_date, 
            "start_time": event.formatted_start, 
            "end_time": event.formatted_end,     
            "booking_code": booking.booking_code,
            "booking_date": booking.booking_time.strftime("%a, %d %b %Y"),
            "booking_time": booking.booking_time.strftime("%I:%M %p"),
            "event_id": event.id,
            "status": event.status,
        }
        if event_end >= now:
            upcoming_booked.append(booking_info)
        else:
            inactive_booked.append(booking_info)

    # Created events by the user
    created_events = (
        Event.query.filter_by(user_id=current_user.id)
        .order_by(Event.date.desc())
        .all()
    )

    upcoming_created = []
    inactive_created = []

    for event in created_events:
        format_info(event)
        event_end = datetime.combine(event.date, event.end_time)
        created_info = {
            "title": event.title,
            "cuisine": event.cuisine,
            "image": event.image_filename,
            "update_event_status": event.update_event_status,
            "date": event.formatted_date,
            "start_time": event.formatted_start,
            "end_time": event.formatted_end,
            "tickets_remaining": event.tickets_remaining(),
            "event_id": event.id,
            "status": event.status,
        }
        if event.update_event_status == "Cancelled" or event_end < now:
            inactive_created.append(created_info)
        else:
            upcoming_created.append(created_info)

    return render_template(
        'booking-history.html',
        upcoming_booked=upcoming_booked,
        inactive_booked=inactive_booked,
        upcoming_created=upcoming_created,
        inactive_created=inactive_created
    )

# Static error page route 
@main_bp.route('/error')
def error():
    return render_template('error.html')

# Error handlers for 404 error 
@main_bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error_code="404 - Page Not Found", 
                           message="The link you followed is broken or the page has been removed."), 404

# Error handler for 500 error
@main_bp.app_errorhandler(500)
def internal_server_error(error):
    return render_template('error.html', error_code="500 - Internal Server Error", 
                           message="Something went wrong on our end. Please try again later."), 500

# Route to search for events by title on home page
@main_bp.route('/search')
def search():
    search_query = request.args.get('q', '')  
    if search_query:
        all_events = Event.query.filter(
            Event.title.ilike(f'%{search_query}%') | Event.description.ilike(f'%{search_query}%')
        ).order_by(Event.date).all()
    else:
        all_events = Event.query.order_by(Event.date).all()

    events = []
    for event in all_events:
        if event.update_event_status in ["Open", "Sold Out"]:
            format_info(event)
            events.append(event)

    return render_template('index.html', events=events, search_query=search_query)

# Simulate a 500 error for testing purposes
@main_bp.route('/trigger-500')
def trigger_500():
    abort(500)