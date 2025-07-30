from flask import Blueprint, render_template, current_app, request
from services.trello_service import fetch_tasks_from_trello
from services.scheduling import generate_schedule
from models.task import Task
from datetime import datetime

page_bp = Blueprint('pages', __name__)

@page_bp.route('/')
def home():
    return render_template('home.html')

@page_bp.route('/tasks-ui')
def tasks_ui():
    # only fetch once per server run
    if not Task._store:
        for d in fetch_tasks_from_trello():
            Task.from_dict(d).save()
    tasks = list(Task._store.values())
    return render_template('tasks.html', tasks=tasks)

@page_bp.route('/schedule-ui')
def schedule_ui():
    if not Task._store:
        for d in fetch_tasks_from_trello():
            Task.from_dict(d).save()

    start_date = request.args.get('startDate', datetime.today().date().isoformat())
    algorithm = request.args.get('alg', 'balanced')
    limit = current_app.config['DAILY_HOUR_LIMIT']
    sched = generate_schedule(start_date, limit, algorithm)

    # prepare events and stats
    events = []
    total_hours = 0
    for day in sched:
        for t in day['tasks']:
            events.append({
                'id': t['id'],
                'title': f"{t['name']} ({t['effort']}h)",
                'start': day['date'],
                'allDay': True,
            })
            total_hours += t['effort']

    stats = {
        'days': len(sched),
        'tasks': len(events),
        'hours': total_hours
    }

    return render_template('schedule.html',
                           events=events,
                           stats=stats,
                           selected_alg=algorithm)

