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
from .utils import format_info, validate_times, check_upload_file

event_bp = Blueprint('events', __name__, url_prefix='/events') 

@event_bp.route('/create-event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = CreateEventForm()
    user_id = current_user.id

    if form.validate_on_submit():
        if not form.image.data:
            flash("Image is required for creating a new event.", "danger")

        errors = validate_times(form.event_date.data, form.start_time.data, form.end_time.data)
        for error in errors:
            if "End time" in error:
                form.end_time.errors.append(error)
            else:
                form.start_time.errors.append(error)

        if not form.image.data or errors:
            return render_template('events/create-event.html', form=form, current_date=date.today())

        image_path = check_upload_file(form)
        new_event = Event(
            title=form.event_name.data,
            description=form.description.data,
            date=form.event_date.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            cuisine=form.cuisine.data,
            location=form.location.data,
            price=form.price.data,
            capacity=form.tickets.data,
            image_filename=image_path,
            user_id=user_id,
            status="Published"
        )

        db.session.add(new_event)
        db.session.commit()
        flash("Event created successfully!", "success")
        return redirect(url_for('main.index'))

    return render_template('events/create-event.html', form=form, current_date=date.today())

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

        flash("Comment successfully posted!", "success")
        return redirect(url_for('events.event_detail', event_id=event.id))

    return render_template('events/event-detail.html', event=event, form=form)

@event_bp.route('edit-event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = db.session.get(Event, event_id)
    if event is None or event.user_id != current_user.id:
        flash("You are not authorized to edit this event.", "danger")
        return redirect(url_for('events.event_detail', event_id=event_id))

    event.event_name = event.title
    event.event_date = event.date

    form = EditEventForm(obj=event)

    if form.validate_on_submit():
        errors = validate_times(form.event_date.data, form.start_time.data, form.end_time.data)
        if errors:
            for error in errors:
                if "End time" in error:
                    form.end_time.errors.append(error)
                else:
                    form.start_time.errors.append(error)
            return render_template(
                'events/create-event.html',
                form=form,
                event=event,
                current_date=date.today(),
                page_title="Edit Event"
            )

        event.title = form.event_name.data
        event.description = form.description.data
        event.date = form.event_date.data
        event.start_time = form.start_time.data 
        event.end_time = form.end_time.data 
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
        'events/create-event.html',
        form=form,
        event=event,
        current_date=date.today(),
        page_title="Edit Event"
    )

@event_bp.route('book-event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def book_event(event_id):
    event = Event.query.get_or_404(event_id)
    form = BookingForm()
    format_info(event)

    if form.validate_on_submit():
        quantity = form.num_tickets.data

        # Prevent overbooking
        if quantity > event.tickets_remaining():
            flash(f"Only {event.tickets_remaining()} tickets remaining. Please reduce your quantity.", 
                  'danger')
            return redirect(url_for('main.booking_history', event_id=event.id))

        # Generate unique booking code
        booking = Booking(
            quantity=quantity,
            user_id=current_user.id,
            event_id=event.id,
        )
        booking.booking_code = booking.generate_booking_code()

        db.session.add(booking)
        

        db.session.commit()

        # need to update redirect to the booking history page
        flash(f"Successfully booked {quantity} ticket(s)! Booking ID: #{booking.booking_code}", 'success')
        return redirect(url_for('main.booking_history')) 

    return render_template('events/book-event.html', event=event, form=form)

@event_bp.route('/cancel-event/<int:event_id>', methods=['POST'])
@login_required
def cancel_event(event_id):
    event = db.session.get(Event, event_id)
    if event is None or event.user_id != current_user.id:
        flash("You are not authorized to cancel this event.", "danger")
        return redirect(url_for('events.event_detail', event_id=event_id))
    event.status = "Cancelled"
    db.session.commit()
    flash("Event has been cancelled.", "success")
    return redirect(url_for('main.index', event_id=event_id))
