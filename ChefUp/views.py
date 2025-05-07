from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/create-event')
def create_event():
    return render_template('create-event.html')

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