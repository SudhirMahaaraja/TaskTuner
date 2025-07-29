from datetime import datetime, timedelta
from models.task import Task
from models.schedule import DaySchedule

def generate_schedule(start_date_str, daily_limit):
    start = datetime.fromisoformat(start_date_str)
    tasks = list(Task._store.values())
    schedule = []
    current_day = DaySchedule(start.date().isoformat())
    remaining = daily_limit

    for task in tasks:
        if task.effort <= remaining:
            current_day.add_task(task)
            remaining -= task.effort
        else:
            schedule.append(current_day.to_dict())
            start += timedelta(days=1)
            current_day = DaySchedule(start.date().isoformat())
            remaining = daily_limit
            if task.effort <= remaining:
                current_day.add_task(task)
                remaining -= task.effort
            else:
                # You could split across days or flag too-large tasks
                pass

    schedule.append(current_day.to_dict())
    return schedule
