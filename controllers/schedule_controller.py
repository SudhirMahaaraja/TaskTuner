from flask import Blueprint, jsonify, request, current_app
from services.scheduling import generate_schedule

schedule_bp = Blueprint('schedule', __name__)

@schedule_bp.route('', methods=['GET'])
def get_schedule():
    start = request.args.get('startDate')
    limit = current_app.config['DAILY_HOUR_LIMIT']
    schedule = generate_schedule(start, limit)
    return jsonify(schedule)
