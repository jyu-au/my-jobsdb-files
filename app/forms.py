from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    """Form for user login"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    """Form for user registration"""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different one.')

class JobForm(FlaskForm):
    """Form for job postings"""
    title = StringField('Job Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Job Description', validators=[DataRequired()])
    requirements = TextAreaField('Job Requirements', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired(), Length(max=100)])
    salary = StringField('Salary', validators=[DataRequired(), Length(max=50)])
    contact_info = StringField('Contact Information', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Post Job')

class ResumeForm(FlaskForm):
    """Form for resume submission"""
    name = StringField('Full Name', validators=[DataRequired(), Length(max=64)])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    education = StringField('Education Level', validators=[DataRequired(), Length(max=100)])
    contact = StringField('Contact Information', validators=[DataRequired(), Length(max=100)])
    experience = TextAreaField('Work Experience', validators=[DataRequired()])
    introduction = TextAreaField('Self Introduction', validators=[DataRequired()])
    submit = SubmitField('Save Resume')

class JobSearchForm(FlaskForm):
    """Form for searching jobs"""
    title = StringField('Job Title')
    location = StringField('Location')
    salary = StringField('Salary Range')
    submit = SubmitField('Search')

class EditProfileForm(FlaskForm):
    """Form for editing user profile"""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Save Changes')

class ChangePasswordForm(FlaskForm):
    """Form for changing user password"""
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long.')
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Passwords must match.')
    ])
    submit = SubmitField('Change Password') 