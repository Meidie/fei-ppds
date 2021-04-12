class Task:
    def __init__(self, task_id, n_iterations):
        self.task_id = task_id
        self.n_iterations = n_iterations

    def run(self):
        yield
        for i in range(self.n_iterations):
            print("Task:", self.task_id)
            yield


class TaskScheduler:
    def __init__(self):
        self.active_tasks = []
        self.scheduled_tasks = []

    def add_task(self, task: Task):
        g = task.run()
        g.send(None)
        self.active_tasks.append((g, task.task_id))

    def schedule(self):
        while self.active_tasks:
            for task in self.active_tasks:
                try:
                    next(task[0])
                    self.scheduled_tasks.append(task)
                except StopIteration:
                    print(f"Task: {task[1]} terminated")
                    continue

            self.active_tasks = self.scheduled_tasks
            self.scheduled_tasks = []


def main():
    t1 = Task(1, 1)
    t2 = Task(2, 2)
    t3 = Task(3, 3)

    ts = TaskScheduler()
    ts.add_task(t1)
    ts.add_task(t2)
    ts.add_task(t3)

    ts.schedule()


if __name__ == "__main__":
    main()
