from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models.models import Shift, Leave, Employee

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """根路由：如果已登入則導向儀表板，否則顯示首頁"""
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('main.admin_dashboard'))
        return redirect(url_for('main.staff_dashboard'))
    return render_template('index.html')

@main_bp.route('/dashboard/staff')
@login_required
def staff_dashboard():
    """員工專屬儀表板：顯示個人班表與請假狀態"""
    # 獲取該員工的所有班表
    my_shifts = Shift.query.filter_by(employee_id=current_user.id).order_by(Shift.start_time).all()
    # 獲取最近的請假申請
    my_leaves = Leave.query.filter_by(employee_id=current_user.id).order_by(Leave.created_at.desc()).limit(5).all()
    
    return render_template('dashboard_staff.html', shifts=my_shifts, leaves=my_leaves)

@main_bp.route('/dashboard/admin')
@login_required
def admin_dashboard():
    """店長專屬儀表板：顯示人力概況與待審核事項"""
    if current_user.role != 'admin':
        return redirect(url_for('main.index'))
    
    # 獲取所有待審核請假
    pending_leaves = Leave.query.filter_by(status='pending').all()
    # 獲取所有草稿班表
    draft_shifts = Shift.query.filter_by(status='draft').all()
    # 統計總員工數
    employee_count = Employee.query.count()
    
    return render_template('dashboard_admin.html', 
                           pending_count=len(pending_leaves),
                           draft_count=len(draft_shifts),
                           employee_count=employee_count)
