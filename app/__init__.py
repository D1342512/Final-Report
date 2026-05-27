from flask import Flask
import os
from .models.models import db

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    # 配置
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'database.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # 確保 instance 資料夾存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 初始化 DB
    db.init_app(app)

    # 初始化 LoginManager
    from flask_login import LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from .models.models import Employee
        return Employee.query.get(int(user_id))

    # 註冊 Blueprints
    from .routes.main import main_bp
    from .routes.scheduler import scheduler_bp
    from .routes.leave import leave_bp
    from .routes.auth import auth_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(scheduler_bp)
    app.register_blueprint(leave_bp)
    app.register_blueprint(auth_bp)

    return app
