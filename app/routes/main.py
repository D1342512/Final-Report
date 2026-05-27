from flask import Blueprint, render_template, request, redirect, url_for, session

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """首頁/儀表板：根據角色顯示不同內容"""
    pass

@main_bp.route('/dashboard/staff')
def staff_dashboard():
    """員工專屬儀表板"""
    pass

@main_bp.route('/dashboard/admin')
def admin_dashboard():
    """店長專屬儀表板"""
    pass
