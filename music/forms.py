from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, IntegerField, DateField, TimeField, SelectField, DecimalField
from wtforms.validators import InputRequired, Email, EqualTo, NumberRange
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}

# Create new event
class EventForm(FlaskForm):
    name = StringField('Event Name', validators=[InputRequired()])
    status = SelectField('Event Status', choices=[
        ('open', 'Open'),
        ('inactive', 'Inactive')
    ], validators=[InputRequired()])
    date = DateField('Event Date', format='%Y-%m-%d', validators=[InputRequired()])
    location = StringField('Event Location', validators=[InputRequired()])
    start_time = TimeField('Start Time', validators=[InputRequired()])
    end_time = TimeField('End Time', validators=[InputRequired()])
    category = SelectField('Event Category', choices=[
        ('concert', 'Concert'),
        ('rock', 'Rock'),
        ('jazz', 'Jazz'),
        ('rap', 'Rap'),
        ('blues', 'Blues'),
        ('hip-hop', 'Hip Hop'),
        ('rnb', 'R and B')
    ])
    price = IntegerField('Event Price (AUD)', validators=[InputRequired()])
    ticketquantity = IntegerField("Quantity of Tickets", validators=[InputRequired()])
    description = TextAreaField('Event Description', validators=[InputRequired()])
    image = FileField('Event Image', validators=[InputRequired()])
    submit_create = SubmitField("Create Event")

#User login
class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

#User register
class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    
    #linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    #submit button
    submit = SubmitField("Register")

#User comment
class CommentForm(FlaskForm):
  text = TextAreaField('Comment', [InputRequired()])
  submit = SubmitField('Create')
  
#Select Event
class EventSelectForm(FlaskForm):
  name = StringField("Event Name", validators=[InputRequired()])
  date = DateField("Date", validators=[InputRequired()])
  time = TimeField("Time", validators=[InputRequired()])
  
#Purchase Ticket
class TicketForm(FlaskForm):
  quant_tickets = IntegerField("Quantity of Tickets", validators=[InputRequired(), NumberRange(min=0)])
  checkout = SubmitField("Checkout")
  
  
