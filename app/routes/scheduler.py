from flask import Blueprint, render_template, request, redirect, url_for

scheduler_bp = Blueprint('scheduler', __name__)

@scheduler_bp.route('/scheduler')
def index():
    """顯示排班設定介面"""
    pass

@scheduler_bp.route('/scheduler/run', methods=['POST'])
def run_scheduler():
    """執行自動排班演算法"""
    pass

@scheduler_bp.route('/scheduler/preview')
def preview_schedule():
    """預覽演算結果"""
    pass

@scheduler_bp.route('/scheduler/publish', methods=['POST'])
def publish_schedule():
    """正式發布班表"""
    pass
