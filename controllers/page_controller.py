# controllers/page_controller.py

from flask import Blueprint, render_template, current_app, request
from services.trello_service import fetch_tasks_from_trello
from services.scheduling import generate_schedule
from models.task import Task
from datetime import datetime

page_bp = Blueprint('pages', __name__)

@page_bp.route('/')
def home():
    # If we don't yet have any tasks in memory, fetch once:
    if not Task._store:
        try:
            tasks_data = fetch_tasks_from_trello()
        except RuntimeError:
            tasks_data = []  # or handle differently

        for d in tasks_data:
            Task.from_dict(d).save()

    # Now render whatever is in memory (including updated efforts!)
    tasks = list(Task._store.values())
    return render_template('tasks.html', tasks=tasks)

@page_bp.route('/view-schedule')
def view_schedule():
    # Make sure we have data first
    if not Task._store:
        # optional: same fetch logic if you want schedule before /
        try:
            for d in fetch_tasks_from_trello():
                Task.from_dict(d).save()
        except RuntimeError:
            pass

    start_date = request.args.get('startDate', datetime.today().date().isoformat())
    limit = current_app.config['DAILY_HOUR_LIMIT']
    schedule = generate_schedule(start_date, limit)
    return render_template('schedule.html', schedule=schedule, start_date=start_date)
