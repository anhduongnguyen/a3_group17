from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from wtforms.fields import  DateField, TimeField, IntegerField, SelectField, FileField
from flask_wtf.file import FileField, FileAllowed
from wtforms import DecimalField, FloatField
from datetime import date


ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}

# creates the login information
class LoginForm(FlaskForm):
    email=StringField("Email Address", validators=[InputRequired('Enter email address')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[InputRequired()])
    surname = StringField("Surname", validators=[InputRequired()])
    email = StringField("Email Address", validators=[
        InputRequired(), 
        Email("Please enter a valid email")
    ])
    contact_number = StringField("Contact Number", validators=[
        InputRequired(), 
        Length(min=10, max=10, message="Enter a valid contact number")
    ])
    street_address = StringField("Address", validators=[
        InputRequired(), 
        Length(max=200)
    ])
    password = PasswordField("Password", validators=[
        InputRequired(),
        EqualTo('confirm', message="Passwords should match")
    ])
    confirm = PasswordField("Confirm Password", validators=[InputRequired()])

    submit = SubmitField("Register")



# this is the form for creating a event
class EventForm(FlaskForm):
    event_name = StringField("Event Name", validators=[InputRequired(), Length(max=60)])
    event_date = DateField(
        "Event Date",
        validators=[InputRequired()],
        format='%Y-%m-%d',
        render_kw={"min": date.today().strftime('%Y-%m-%d')}
    )
    start_time = TimeField("Start Time", validators=[InputRequired()])
    end_time = TimeField("End Time", validators=[InputRequired()])
    cuisine = SelectField("Cuisine Type", choices=[
        ('Italian', 'Italian'), ('Japanese', 'Japanese'), ('Mexican', 'Mexican'),
        ('Korean', 'Korean'), ('Vietnamese', 'Vietnamese'), ('Thai', 'Thai'),
        ('Indian', 'Indian'), ('Chinese', 'Chinese'), ('Other', 'Other')], validators=[InputRequired()])
    tickets = IntegerField("Number of Tickets", validators=[InputRequired()], default=1)
    price = FloatField("Price (AUD)", validators=[InputRequired()])
    location = StringField("Location", validators=[InputRequired(), Length(max=200)])
    description = TextAreaField("Description", validators=[InputRequired()])
    image = FileField("Image Upload", validators=[
        FileAllowed(ALLOWED_FILE, 'Only image files are allowed (jpg, png, jpeg)')])
    submit = SubmitField("Submit")
