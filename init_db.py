from app import create_app
from app.models.models import db, Employee

app = create_app()

with app.app_context():
    # 建立所有資料表
    db.create_all()
    
    # 建立預設店長帳號 (如果不存在)
    if not Employee.query.filter_by(username='admin').first():
        admin = Employee(
            username='admin',
            name='系統管理員',
            role='admin',
            skill_type='management'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("資料庫已初始化，預設店長帳號：admin / admin123")
    else:
        print("資料庫已存在，無需初始化。")
