from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.models import db, Shift, Employee, Leave
from datetime import datetime, timedelta

scheduler_bp = Blueprint('scheduler', __name__)

@scheduler_bp.route('/scheduler')
@login_required
def index():
    """顯示排班設定介面"""
    if current_user.role != 'admin':
        return redirect(url_for('main.index'))
    
    # 獲取目前的草稿班表
    draft_shifts = Shift.query.filter_by(status='draft').all()
    # 獲取員工清單
    employees = Employee.query.all()
    
    return render_template('scheduler/index.html', drafts=draft_shifts, employees=employees)

@scheduler_bp.route('/scheduler/run', methods=['POST'])
@login_required
def run_scheduler():
    """執行自動排班演算法 (簡易演示版)"""
    if current_user.role != 'admin':
        return redirect(url_for('main.index'))
    
    # 清除現有的草稿
    Shift.query.filter_by(status='draft').delete()
    
    employees = Employee.query.all()
    if not employees:
        flash('沒有員工資料，無法排班。', 'warning')
        return redirect(url_for('scheduler.index'))
    
    # 模擬排班：未來 7 天，每天兩個班次 (09:00-13:00, 13:00-17:00)
    start_date = datetime.now() + timedelta(days=1)
    start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
    
    count = 0
    for day in range(7):
        current_day = start_date + timedelta(days=day)
        
        # 時段：早班與晚班
        slots = [
            (current_day.replace(hour=9), current_day.replace(hour=13)),
            (current_day.replace(hour=13), current_day.replace(hour=17))
        ]
        
        for idx, slot in enumerate(slots):
            # 輪流分配員工 (簡易邏輯)
            emp = employees[(day * 2 + idx) % len(employees)]
            
            # 檢查是否與請假衝突 (簡易檢查：只要時段重疊就不排)
            on_leave = Leave.query.filter(
                Leave.employee_id == emp.id,
                Leave.status == 'approved',
                Leave.start_time <= slot[1],
                Leave.end_time >= slot[0]
            ).first()
            
            if not on_leave:
                new_shift = Shift(
                    employee_id=emp.id,
                    start_time=slot[0],
                    end_time=slot[1],
                    status='draft'
                )
                db.session.add(new_shift)
                count += 1
                
    db.session.commit()
    flash(f'自動排班運算完成！已生成 {count} 筆草稿班表。', 'success')
    return redirect(url_for('scheduler.index'))

@scheduler_bp.route('/scheduler/publish', methods=['POST'])
@login_required
def publish_schedule():
    """正式發布班表"""
    if current_user.role != 'admin':
        return redirect(url_for('main.index'))
    
    drafts = Shift.query.filter_by(status='draft').all()
    for s in drafts:
        s.status = 'published'
        
    db.session.commit()
    flash(f'成功發布 {len(drafts)} 筆班表！員工現在可以在儀表板查看。', 'success')
    return redirect(url_for('main.index'))
