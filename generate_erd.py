import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_schemadisplay import create_schema_graph

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////workspaces/my-jobsdb-files/instance/jobsdb.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 从 models.py 导入所有模型
from app.models import User, Job, Resume  # 根据实际路径调整

with app.app_context():
    # 检查数据库文件是否存在
    db_file = '/workspaces/my-jobsdb-files/instance/jobsdb.sqlite'
    if not os.path.exists(db_file):
        open(db_file, 'w').close()  # 创建空文件
    
    # 创建表（首次运行）
    db.create_all()

    # 生成关系图
    graph = create_schema_graph(
        metadata=db.metadata,
        engine=db.engine,
        show_datatypes=True,
        show_indexes=True,
        rankdir='TB'
    )
    graph.write_png('erd.png')
    print("ER 图已生成到 erd.png")