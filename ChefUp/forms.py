from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, NumberRange, EqualTo, Regexp
from wtforms.fields import  DateField, TimeField, IntegerField, SelectField, FileField
from flask_wtf.file import FileField, FileAllowed
from wtforms import DecimalField, FloatField
from datetime import date


ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}

CUISINE_CHOICES = [
    ('Italian', 'Italian'), ('Japanese', 'Japanese'), ('Mexican', 'Mexican'),
    ('Korean', 'Korean'), ('Vietnamese', 'Vietnamese'), ('Thai', 'Thai'),
    ('Indian', 'Indian'), ('Chinese', 'Chinese'), ('French', 'French'),
    ('Spanish', 'Spanish'), ('Greek', 'Greek'), ('American', 'American'),
    ('Middle Eastern', 'Middle Eastern'), ('Caribbean', 'Caribbean'),
    ('African', 'African'), ('Other', 'Other')
]

# creates the login information
class LoginForm(FlaskForm):
    email=StringField("Email Address", validators=[InputRequired('Email address is required'),])
    password=PasswordField("Password", validators=[InputRequired('Password is required')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[InputRequired("First name is required")])
    surname = StringField("Surname", validators=[InputRequired("Surname is required")])
    email = StringField("Email Address", validators=[
        InputRequired("Email address is required"), 
        Regexp(
            r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$',
            message="Enter a valid email address (e.g., user@example.com)"
        )
    ])
    contact_number = StringField("Contact Number", validators=[
        InputRequired("Contact number is required"), 
        Length(min=10, max=10, message="Enter a valid contact number")
    ])
    street_address = StringField("Address", validators=[
        InputRequired("Street address is required"), 
        Length(max=200)
    ])
    password = PasswordField("Password", validators=[
        InputRequired("Password is required"),
        EqualTo('confirm', message="Passwords should match")
    ])
    confirm = PasswordField("Confirm Password", validators=[InputRequired("Please confirm your password")])

    submit = SubmitField("Register")

# this is the form for creating a event
class CreateEventForm(FlaskForm):
    event_name = StringField("Event Name", validators=[
        InputRequired("Event name is required"), 
        Length(max=60)])
    event_date = DateField(
        "Event Date",
        validators=[InputRequired("Event date is required")],
        format='%Y-%m-%d',
        render_kw={"min": date.today().strftime('%Y-%m-%d')}
    )
    start_time = TimeField("Start Time", validators=[InputRequired("Start time is required")])
    end_time = TimeField("End Time", validators=[InputRequired("End time is required")])
    cuisine = SelectField("Cuisine Type", choices=[
        ('', 'Select cuisine'),  
        *CUISINE_CHOICES], 
        validators=[InputRequired("Cuisine type is required")])
    tickets = IntegerField("Number of Tickets", validators=[
        InputRequired("Number of tickets mmust be set")], default=1)
    price = FloatField("Price (AUD)", validators=[InputRequired("Price is required")])
    location = StringField("Location", validators=[
        InputRequired("Event Location is required"), 
        Length(max=200)])
    description = TextAreaField("Description", validators=[
        InputRequired("Event description is required")])
    image = FileField("Image Upload", validators=[
        FileAllowed(ALLOWED_FILE, 'Only image files are allowed (jpg, png, jpeg)'), 
        InputRequired("Please upload an image for your event")])    
    submit = SubmitField("Submit")

class EditEventForm(FlaskForm):
    event_name = StringField("Event Name", validators=[
        InputRequired("Event name is required"), 
        Length(max=60)])
    event_date = DateField(
        "Event Date",
        validators=[InputRequired("Event date is required")],
        format='%Y-%m-%d',
        render_kw={"min": date.today().strftime('%Y-%m-%d')}
    )
    start_time = TimeField("Start Time", validators=[InputRequired("Start Time is required")])
    end_time = TimeField("End Time", validators=[InputRequired("End Time is required")])
    cuisine = SelectField("Cuisine Type", choices=[
        ('', 'Select cuisine'), 
        *CUISINE_CHOICES
        ], validators=[InputRequired("Cuisine type is required")])
    tickets = IntegerField("Number of tickets mmust be set", validators=[
        InputRequired("")], default=1)
    price = FloatField("Price (AUD)", validators=[InputRequired("Price is required")])
    location = StringField("Location", validators=[
        InputRequired(), 
        Length(max=200)])
    description = TextAreaField("Description", validators=[
        InputRequired("Event description is required")])
    image = FileField("Image Upload", validators=[
        FileAllowed(ALLOWED_FILE, 'Only image files are allowed (jpg, png, jpeg)')])
    submit = SubmitField("Submit")

class CommentingForm(FlaskForm):
    content = TextAreaField("Comment", validators=[InputRequired(), Length(max=500)])
    submit = SubmitField("Post")
    
class BookingForm(FlaskForm):
    num_tickets = IntegerField("Number of Tickets", default=1, validators=[
        InputRequired("Number of tickets is required"), 
        NumberRange(min=1, message="At least one ticket must be booked")])
    submit = SubmitField('Confirm Booking')
        