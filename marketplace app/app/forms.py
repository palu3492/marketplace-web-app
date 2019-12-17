from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User
from flask_wtf.file import FileField, FileAllowed, FileRequired

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida',
    'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland',
    'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New',
    'Hampshire', 'New', 'Jersey', 'New', 'Mexico', 'New', 'York', 'North', 'Carolina', 'North', 'Dakota', 'Ohio',
    'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode', 'Island', 'South', 'Carolina', 'South', 'Dakota', 'Tennessee',
    'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West', 'Virginia', 'Wisconsin', 'Wyoming']
state_choices = []
for state in states:
   state_choices.append((state, state))

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    state = SelectField('State', choices=state_choices)
    city = StringField('City', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('There is an existing account with that email.')

class EditProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    state = SelectField('State', choices=state_choices)
    city = StringField('City', validators=[DataRequired()])
    submit = SubmitField('Submit')

    # def __init__(self, original_name, *args, **kwargs):
    #     super(EditProfileForm, self).__init__(*args, **kwargs)
    #     self.original_name = original_name

    # def validate_username(self, username):
    #     if username.data != self.original_username:
    #         user = User.query.filter_by(username=self.username.data).first()
    #         if user is not None:
    #             raise ValidationError('Please use a different username.')


class ListingForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=140)])
    body = TextAreaField('Details', validators=[DataRequired(), Length(min=1, max=1000)])
    price = StringField('Price', validators=[DataRequired()])
    conditions = [('New','New'), ('Used', 'Used'), ('Broken', 'Broken')]
    condition = SelectField('Condition', choices=conditions)
    image = FileField('Image')
    submit = SubmitField('Submit')

class MessageForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired(), Length(min=1, max=140)])
    body = TextAreaField('Message', validators=[DataRequired(), Length(min=1, max=1000)])
    submit = SubmitField('Submit')

class FilterForm(FlaskForm):
    price_min = StringField('Price min')
    price_max = StringField('Price max')
    conditions = [('', ''), ('New','New'), ('Used', 'Used'), ('Broken', 'Broken')]
    condition = SelectField('Condition', choices=conditions)
    submit = SubmitField('Submit')

