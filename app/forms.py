from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional
from app.models import User, Job, Resume, Application, JobSkill, Language, Feedback, NotificationTemplate, Config, StaticContent, Tag, Country, Industry

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


class JobSkillForm(FlaskForm):
    """Form for job skills"""
    skill_name = StringField('Skill Name', validators=[
        DataRequired(),
        Length(max=50, message="Skill name cannot be longer than 50 characters")
    ])
    importance = SelectField('Importance', choices=[
        ('required', 'Required'),
        ('preferred', 'Preferred'),
        ('plus', 'Nice to Have')
    ], validators=[DataRequired()])
    submit = SubmitField('Add Skill')

    def validate_skill_name(self, field):
        if JobSkill.query.filter_by(skill_name=field.data).first():
            raise ValidationError('This skill already exists')

class LanguageForm(FlaskForm):
    """Form for languages"""
    name = StringField('Language', validators=[DataRequired(), Length(max=50)])
    proficiency_level = SelectField('Proficiency', choices=[
        ('native', 'Native'),
        ('fluent', 'Fluent'),
        ('intermediate', 'Intermediate'),
        ('basic', 'Basic')
    ], validators=[DataRequired()])
    submit = SubmitField('Add Language')

class FeedbackForm(FlaskForm):
    """Form for feedback"""
    contact = StringField('Contact (Optional)', validators=[Optional(), Length(max=100)])
    content = TextAreaField('Feedback Content', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('bug', 'Bug Report'),
        ('suggestion', 'Feature Suggestion'),
        ('compliment', 'Compliment')
    ], validators=[DataRequired()])
    submit = SubmitField('Submit Feedback')

class NotificationTemplateForm(FlaskForm):
    """Form for notification templates"""
    template_name = StringField('Template Name', validators=[DataRequired(), Length(max=50)])
    subject = StringField('Email Subject', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Email Content', validators=[DataRequired()])
    submit = SubmitField('Save Template')

class ConfigForm(FlaskForm):
    """Form for system configs"""
    key = StringField('Config Key', validators=[DataRequired(), Length(max=50)])
    value = StringField('Config Value', validators=[DataRequired(), Length(max=200)])
    description = StringField('Description', validators=[Optional(), Length(max=255)])
    submit = SubmitField('Save Config')

class StaticContentForm(FlaskForm):
    """Form for static pages"""
    page_name = StringField('Page Name', validators=[DataRequired(), Length(max=50)])
    title = StringField('Page Title', validators=[DataRequired(), Length(max=100)])
    body = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Save Content')

class TagForm(FlaskForm):
    """Form for tags"""
    name = StringField('Tag Name', validators=[DataRequired(), Length(max=30)])
    color = StringField('Color (Hex)', validators=[DataRequired(), Length(min=7, max=7)])
    submit = SubmitField('Create Tag')

class CountryForm(FlaskForm):
    """Form for countries"""
    name = StringField('Country Name', validators=[DataRequired(), Length(max=50)])
    code = StringField('Country Code (2 letters)', validators=[DataRequired(), Length(min=2, max=2)])
    phone_code = StringField('Phone Code', validators=[Optional(), Length(max=5)])
    submit = SubmitField('Add Country')

class IndustryForm(FlaskForm):
    """Form for industries"""
    name = StringField('Industry Name', validators=[DataRequired(), Length(max=50)])
    description = StringField('Description', validators=[Optional(), Length(max=255)])
    submit = SubmitField('Add Industry')