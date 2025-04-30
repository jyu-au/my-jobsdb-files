from app import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# User roles
class Role:
    USER = 'user'
    ADMIN = 'admin'

class User(UserMixin, db.Model):
    """User model for job seekers and admins"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(512))
    role = db.Column(db.String(10), default=Role.USER)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    resumes = db.relationship('Resume', backref='user', lazy='dynamic')
    applications = db.relationship('Application', backref='applicant', lazy='dynamic')
    
    def __init__(self, username, email, password, role=Role.USER):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.role = role
    
    def check_password(self, password):
        """Check if the provided password matches the stored hash"""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """Check if the user has admin role"""
        return self.role == Role.ADMIN
    
    def __repr__(self):
        return f'<User {self.username}>'

    def has_applied_to(self, job_id):
        """Check if the user has already applied to a specific job"""
        return Application.query.filter_by(
            user_id=self.id,
            job_id=job_id
        ).first() is not None

    def set_password(self, password):
        """Set password for user"""
        self.password_hash = generate_password_hash(password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Job(db.Model):
    """Job posting model"""
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text(65535), nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.String(50), nullable=False)
    contact_info = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    posted_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    required_skills = db.relationship('JobSkill', backref='job_skills', lazy='dynamic')
    preferred_languages = db.relationship('Language', secondary='job_languages', backref='jobs')
    skills = db.relationship('JobSkill', backref='job', lazy='dynamic')
    languages = db.relationship('Language', backref='job', lazy='dynamic')
    tags = db.relationship('Tag', secondary='job_tags', backref='jobs')
    
    # Relationships
    applications = db.relationship('Application', backref='job', lazy='dynamic')
    poster_user = db.relationship('User', foreign_keys=[posted_by], backref='posted_jobs')
    
    def __repr__(self):
        return f'<Job {self.title}>'

class Resume(db.Model):
    """Resume model for job seekers"""
    __tablename__ = 'resumes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    education = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.Text, nullable=False)
    introduction = db.Column(db.Text(16777215), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    job_languages = db.Table('job_languages',
    db.Column('job_id', db.Integer, db.ForeignKey('jobs.id'), primary_key=True),
    db.Column('language_id', db.Integer, db.ForeignKey('languages.id'), primary_key=True)
    )
    # Relationships
    applications = db.relationship('Application', backref='resume', lazy='dynamic')
    
    def __repr__(self):
        return f'<Resume {self.name}>'

class Application(db.Model):
    """Application model connecting users, jobs, and resumes"""
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=False)
    status = db.Column(db.Enum('Pending', 'Reviewed', 'Accepted', 'Rejected', name='application_status'), 
                      default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Application {self.id}>' 
    
class JobSkill(db.Model):
    __tablename__ = 'job_skills'
    
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'))
    skill_name = db.Column(db.String(50), nullable=False)
    importance = db.Column(db.String(20))  # 'required', 'preferred', 'plus' 

    

class Language(db.Model):
    __tablename__ = 'languages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    proficiency_level = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Language {self.name}>'
    
class SystemLog(db.Model):
    __tablename__ = 'system_logs'
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(50), nullable=False)  # 如login/error/config_change
    description = db.Column(db.Text)
    ip_address = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Feedback(db.Model):
    __tablename__ = 'feedbacks'
    id = db.Column(db.Integer, primary_key=True)
    contact = db.Column(db.String(100))  # 可选联系方式
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(20))  # bug/suggestion/compliment
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class NotificationTemplate(db.Model):
    __tablename__ = 'notification_templates'
    id = db.Column(db.Integer, primary_key=True)
    template_name = db.Column(db.String(50), unique=True)  # application_received/status_update
    subject = db.Column(db.String(200))
    content = db.Column(db.Text, nullable=False)

class Config(db.Model):
    __tablename__ = 'configs'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True)  # maintenance_mode/max_login_attempts
    value = db.Column(db.String(200))
    description = db.Column(db.String(255))

class StaticContent(db.Model):
    __tablename__ = 'static_contents'
    id = db.Column(db.Integer, primary_key=True)
    page_name = db.Column(db.String(50))  # about/terms/privacy
    title = db.Column(db.String(100))
    body = db.Column(db.Text, nullable=False)

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)  # IT/Finance/Engineering
    color = db.Column(db.String(7))  # HEX颜色码

class Country(db.Model):
    __tablename__ = 'countries'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    code = db.Column(db.String(2))  # ISO代码
    phone_code = db.Column(db.String(5))

class Industry(db.Model):
    __tablename__ = 'industries'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)  # 科技/金融/医疗
    description = db.Column(db.String(255))

class Job(db.Model):
    # ... 原有字段
    skills = db.relationship('JobSkill', backref='job', lazy='dynamic')
    languages = db.relationship('Language', backref='job', lazy='dynamic')
    tags = db.relationship('Tag', secondary='job_tags', backref='jobs')

class JobTag(db.Model):
    __tablename__ = 'job_tags'
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)