from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.models import db, Leave, Employee
from datetime import datetime

leave_bp = Blueprint('leave', __name__)

@leave_bp.route('/leave', methods=['GET', 'POST'])
@login_required
def apply_leave():
    """員工請假申請"""
    if request.method == 'POST':
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')
        reason = request.form.get('reason')
        
        try:
            start_time = datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M')
            end_time = datetime.strptime(end_date_str, '%Y-%m-%dT%H:%M')
            
            new_leave = Leave(
                employee_id=current_user.id,
                start_time=start_time,
                end_time=end_time,
                reason=reason,
                status='pending'
            )
            db.session.add(new_leave)
            db.session.commit()
            flash('請假申請已提交，請靜候店長審核。', 'success')
            return redirect(url_for('main.index'))
        except ValueError:
            flash('日期格式錯誤，請重新確認。', 'danger')
            
    return render_template('leave/apply.html')

@leave_bp.route('/admin/leaves')
@login_required
def admin_leaves():
    """店長審核請假清單"""
    if current_user.role != 'admin':
        return redirect(url_for('main.index'))
    
    pending_leaves = Leave.query.filter_by(status='pending').order_by(Leave.created_at.asc()).all()
    history_leaves = Leave.query.filter(Leave.status != 'pending').order_by(Leave.created_at.desc()).limit(20).all()
    
    # 獲取員工姓名對照表 (優化查詢)
    employees = {e.id: e.name for e in Employee.query.all()}
    
    return render_template('admin/leaves.html', pending=pending_leaves, history=history_leaves, employees=employees)

@leave_bp.route('/admin/leaves/audit/<int:leave_id>/<string:status>', methods=['POST'])
@login_required
def audit_leave(leave_id, status):
    """執行准駁操作"""
    if current_user.role != 'admin':
        return redirect(url_for('main.index'))
    
    leave = Leave.query.get_or_404(leave_id)
    if status in ['approved', 'rejected']:
        leave.status = status
        db.session.commit()
        flash(f'已將請假編號 {leave_id} 標記為 {status}。', 'info')
    
    return redirect(url_for('leave.admin_leaves'))
