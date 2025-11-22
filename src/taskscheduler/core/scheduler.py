from typing import List, Dict, Tuple, Optional, Any, Callable
from datetime import datetime
import time

from threading import Lock, Thread
from concurrent.futures import ThreadPoolExecutor

from src.taskscheduler.models import Status, Priority, Task

class Scheduler:
    """Represents the scheduler class"""
    def __init__(self):
        self._lock = Lock()
        self._executor = ThreadPoolExecutor(max_workers=5)
        self._tasks_map: Dict[str, Task] = {}
        self._running = False
    
    def start(self):
        self._running = True
        t1 = Thread(target=self._run_loop, daemon=True)
        t1.start()

    def stop(self):
        self._running = False
        self._executor.shutdown()
    
    def _run_loop(self):
        while self._running:
            time.sleep(1)
            with self._lock:
                tasks_to_check = list(self._tasks_map.values())
                for task in tasks_to_check:
                    if task.status == Status.PENDING and task.scheduled_time <= datetime.now():
                        flag = True
                        for dep_id in task.dependencies:
                            if dep_id not in self._tasks_map or self._tasks_map[dep_id].status != Status.SUCCESS:
                                flag = False
                                break
                            
                        if flag:
                                task.status = Status.RUNNING
                                self._executor.submit(task.target_function, *task.args, **task.kwargs)
            

    def add_task(self, task: Task):
        with self._lock:
            if task.task_id in self._tasks_map:
                raise ValueError(f"Task with ID {task.task_id} already exists")
            else:
                self._tasks_map[task.task_id] = task

    def get_task(self, task_id: str):
        with self._lock:
            if task_id in self._tasks_map:
                return self._tasks_map[task_id]
            else:
                raise ValueError(f"Task with ID {task_id} not found")

    def remove_task(self, task_id: str):
        with self._lock:
            if task_id in self._tasks_map:
                self._tasks_map.pop(task_id)
            else:
                raise ValueError(f"Task with ID {task_id} not found")
