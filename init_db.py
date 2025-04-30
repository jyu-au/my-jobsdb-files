from app import create_app, db
from app.models import User, Job, Resume  # 导入所有模型

app = create_app()

with app.app_context():
    # 删除所有表（谨慎操作，仅用于开发环境）
    db.drop_all()
    
    # 创建所有表
    db.create_all()
    
    print("数据库表已成功创建！")