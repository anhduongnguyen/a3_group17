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

options = [
    'Italian', 'Japanese', 'Mexican',
    'Korean', 'Vietnamese', 'Thai',
    'Indian', 'Chinese', 'French',
    'Spanish', 'Greek', 'Caribbean',
    'Other'
]

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    selected_option = request.args.get('options')  
    filter_message = None
    if selected_option:
        events = Event.query.filter_by(cuisine=selected_option).order_by(Event.date).all()
        if not events:
            filter_message = f'No events found for "{selected_option}" cuisine.'
    else:
        events = Event.query.order_by(Event.date).all()

    for event in events:
        format_info(event)

    return render_template('index.html', events=events, options=options, 
                           selected_option=selected_option, filter_message=filter_message)

@main_bp.route('/booking-history')
def booking_history():
    return render_template('booking-history.html')

@main_bp.route('/error')
def error():
    return render_template('error.html')

@main_bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error_code="404 - Page Not Found", 
                           message="The link you followed is broken or the page has been removed."), 404

@main_bp.app_errorhandler(500)
def internal_server_error(error):
    return render_template('error.html', error_code="500 - Internal Server Error", 
                           message="Something went wrong on our end. Please try again later."), 500


@main_bp.route('/search')
def search():
    search_query = request.args.get('q', '')  
    if search_query:
        events = Event.query.filter(
            Event.title.ilike(f'%{search_query}%') | Event.description.ilike(f'%{search_query}%')
        ).order_by(Event.date).all()
    else:
        events = Event.query.order_by(Event.date).all()

    for event in events:
        format_info(event) 

    return render_template('index.html', events=events, search_query=search_query)

# Simulate a 500 error for testing purposes
@main_bp.route('/trigger-500')
def trigger_500():
    abort(500)