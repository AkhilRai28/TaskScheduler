import pytest
import time
from datetime import datetime, timedelta
from typing import List

from src.taskscheduler.models import Priority, Status, Task
from src.taskscheduler.core import Scheduler

@pytest.fixture
def scheduler_fixture():
    schedule = Scheduler()
    yield schedule
    schedule.stop()

def worker_function(result_log: List, value: str):
    result_log.append(value)

def test_lifecycle(scheduler_fixture):
    results = []
    task = Task(
        target_function=worker_function,
        title="Testing Task 1",
        scheduled_time=datetime.now() -timedelta(seconds=1),
        args=(results,"done")
    )
    scheduler_fixture.add_task(task)
    scheduler_fixture.start()
    time.sleep(1.2)

    assert scheduler_fixture._running == True 
    assert task.status == Status.RUNNING

    scheduler_fixture.stop()

    assert scheduler_fixture._running == False
    assert "done" in results 
