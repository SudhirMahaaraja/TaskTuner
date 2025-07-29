class DaySchedule:
    def __init__(self, date):
        self.date = date
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def to_dict(self):
        return {
            'date': self.date,
            'tasks': [t.to_dict() for t in self.tasks]
        }
