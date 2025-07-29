# controllers/task_controller.py

from flask import Blueprint, jsonify, request
from services.trello_service import fetch_tasks_from_trello
from models.task import Task

task_bp = Blueprint('tasks', __name__)

@task_bp.route('', methods=['GET'])
def get_tasks():
    Task._store.clear()
    for d in fetch_tasks_from_trello():
        Task.from_dict(d).save()
    return jsonify([t.to_dict() for t in Task._store.values()])

@task_bp.route('/effort', methods=['POST'])
def set_effort():
    data = request.get_json()
    # accept either one object or list
    items = data if isinstance(data, list) else [data]
    updated = []
    for item in items:
        task = Task.get(item.get('taskId'))
        if task:
            task.effort = item.get('hours', 0)
            task.save()
            updated.append(task.to_dict())
    return jsonify(updated), 200
