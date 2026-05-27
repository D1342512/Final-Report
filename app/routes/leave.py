from flask import Blueprint, render_template, request, redirect, url_for

leave_bp = Blueprint('leave', __name__)

@leave_bp.route('/leave')
def apply_leave():
    """員工請假表單頁面"""
    pass

@leave_bp.route('/leave/submit', methods=['POST'])
def submit_leave():
    """提交請假申請"""
    pass

@leave_bp.route('/admin/leaves')
def admin_leaves():
    """店長審核請假清單頁面"""
    pass

@leave_bp.route('/admin/leaves/audit/<int:leave_id>/<string:status>', methods=['POST'])
def audit_leave(leave_id, status):
    """執行准駁操作"""
    pass
