import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Secret key for session management and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI = 'sqlite:///apps_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload folder for resumes
    UPLOAD_FOLDER = os.path.join(basedir, 'app/static/uploads')
    
    # Allowed extensions for resume uploads
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'} 

    
# 建议在 config.py 中添加这些防护措施
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
UPLOAD_FOLDER = os.path.join(basedir, 'app/static/uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # 确保上传目录存在