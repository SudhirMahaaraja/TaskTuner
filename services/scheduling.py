from datetime import datetime, timedelta
from models.task import Task
from models.schedule import DaySchedule

def generate_schedule(start_date_str, daily_limit, algorithm='balanced'):
    start = datetime.fromisoformat(start_date_str)

    tasks = list(Task._store.values())
    if algorithm == 'largest':
        tasks.sort(key=lambda t: t.effort, reverse=True)
    elif algorithm == 'smallest':
        tasks.sort(key=lambda t: t.effort)
    # balanced: keep insertion order

    schedule = []
    current_day = DaySchedule(start.date().isoformat())
    remaining = daily_limit

    for task in tasks:
        effort = task.effort
        # split if > limit
        while effort > 0:
            if effort <= remaining:
                split = Task(task.id, task.name, effort)
                current_day.add_task(split)
                remaining -= effort
                effort = 0
            else:
                if remaining > 0:
                    split = Task(task.id, task.name, remaining)
                    current_day.add_task(split)
                    effort -= remaining
                schedule.append(current_day.to_dict())
                start += timedelta(days=1)
                current_day = DaySchedule(start.date().isoformat())
                remaining = daily_limit
    schedule.append(current_day.to_dict())
    return schedule
