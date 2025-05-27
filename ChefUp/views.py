from datetime import datetime
from flask import Blueprint, current_app, render_template, request, flash, redirect, url_for
from flask import abort
from flask_login import current_user, login_required
from .forms import CommentingForm, EditEventForm, CreateEventForm
from . import db
import os
from werkzeug.utils import secure_filename
from .models import Event, Booking, Comment, User
from datetime import date
from .utils import format_info

options = [
    'Italian',
    'Japanese',
    'Mexican',
    'Korean',
    'Vietnamese',
    'Thai',
    'Indian',
    'Chinese',
    'French',
    'Spanish',
    'Greek',
    'American',
    'Middle Eastern',
    'Caribbean',
    'African',
    'Other'
]

main_bp = Blueprint('main', __name__)

event_bp = Blueprint('events', __name__, url_prefix='/events') 

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

    return render_template('index.html', events=events, options=options, selected_option=selected_option, filter_message=filter_message)



@event_bp.route('/create-event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = CreateEventForm()
    user_id = current_user.id

    if form.validate_on_submit():
        # Require image upload for new events
        if not form.image.data:
            flash("Image is required for creating a new event.", "danger")
            return render_template('create-event.html', form=form, current_date=date.today().strftime('%Y-%m-%d'))

        # Save uploaded image
        image_path = check_upload_file(form)

        # Create new event
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
            user_id=user_id,
            status='Open'
        )

        db.session.add(new_event)
        db.session.commit()
        flash("Event created successfully!", "success")
        return redirect(url_for('main.index'))

    # On GET or failed POST
    return render_template('create-event.html', form=form, current_date=date.today().strftime('%Y-%m-%d'))


@main_bp.route('/booking-history')
def booking_history():
    return render_template('booking-history.html')

@event_bp.route('/<int:event_id>', methods=['GET', 'POST'])
def event_detail(event_id):
    event = db.session.get(Event, event_id)
    if event is None:
        abort(404)
    
    format_info(event)  
    form = CommentingForm()
    if form.validate_on_submit():
        new_comment = Comment(
            content=form.content.data,
            user_id=current_user.id,
            event_id=event.id
        )
        db.session.add(new_comment)
        db.session.commit()
       
        return redirect(url_for('events.event_detail', event_id=event.id))

    return render_template('event-detail.html', event=event, form=form)
    
@event_bp.route('/book-event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def book_event(event_id):
    event = Event.query.get_or_404(event_id)
    if request.method == 'POST':
        quantity = int(request.form.get('quantity', 1))
        if event.capacity < quantity:
            flash('Not enough tickets available.', 'danger')
            return redirect(url_for('events.book_event', event_id=event_id))
        booking = Booking(
            user_id=current_user.id,
            event_id=event.id,
            quantity=quantity,
            price_total=(event.price * quantity) + 5,
            booking_time=datetime.now()
        )
    
  
        event.capacity -= quantity
        db.session.add(booking)
        db.session.commit()
        flash(f'Booking confirmed! Your order ID is {booking.id}.', 'success')
        return redirect(url_for('main.booking_history'))
    return render_template('book-event.html', event=event)   

@main_bp.route('/error')
def error():
    return render_template('error.html')


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

@event_bp.route('edit-event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = db.session.get(Event, event_id)
    if event is None or event.user_id != current_user.id:
        flash("You are not authorized to edit this event.", "danger")
        return redirect(url_for('events.event_detail', event_id=event_id))

    event.start_time = datetime.strptime(event.start_time, '%H:%M').time()
    event.end_time = datetime.strptime(event.end_time, '%H:%M').time()

    event.event_name = event.title
    event.event_date = event.date

    form = EditEventForm(obj=event)

    if form.validate_on_submit():
        event.title = form.event_name.data
        event.description = form.description.data
        event.date = form.event_date.data
        event.start_time = form.start_time.data.strftime('%H:%M')
        event.end_time = form.end_time.data.strftime('%H:%M')
        event.cuisine = form.cuisine.data
        event.location = form.location.data
        event.price = form.price.data
        event.capacity += form.tickets.data

        if form.image.data:
            event.image_filename = check_upload_file(form)

        db.session.commit()
        flash("Event updated successfully!", "success")
        return redirect(url_for('events.event_detail', event_id=event.id))

    return render_template(
        'create-event.html',
        form=form,
        event=event,
        current_date=date.today().strftime('%Y-%m-%d'),
        page_title="Edit Event"
    )
   
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