from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import SystemLog, Feedback, NotificationTemplate, Config, StaticContent, Tag, Country, Industry

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# 公共路由 - 静态内容展示
@main.route('/page/<page_name>')
def show_static_page(page_name):
    page = StaticContent.query.filter_by(page_name=page_name).first()
    return render_template('static_page.html', page=page)

# 管理员路由组
@admin_bp.before_request
@login_required
def check_admin():
    if not current_user.is_admin():
        abort(403)

# 系统日志列表
@admin_bp.route('/logs')
def system_logs():
    logs = SystemLog.query.order_by(SystemLog.created_at.desc()).limit(100).all()
    return render_template('admin/logs.html', logs=logs)

# 反馈管理
@admin_bp.route('/feedbacks')
def feedbacks():
    feedback_list = Feedback.query.order_by(Feedback.created_at.desc()).all()
    return render_template('admin/feedbacks.html', feedbacks=feedback_list)

# 系统配置管理
@admin_bp.route('/configs')
def configs():
    config_items = Config.query.all()
    return render_template('admin/configs.html', configs=config_items)

# 通知模板管理
@admin_bp.route('/notification-templates')
def notification_templates():
    templates = NotificationTemplate.query.all()
    return render_template('admin/templates.html', templates=templates)

# 基础数据管理（标签/国家/行业）
@admin_bp.route('/<data_type>')
def manage_data(data_type):
    model = {
        'tags': Tag,
        'countries': Country,
        'industries': Industry
    }.get(data_type)
    
    if not model:
        abort(404)
        
    items = model.query.all()
    return render_template('admin/data_list.html', 
                         items=items,
                         data_type=data_type.capitalize())