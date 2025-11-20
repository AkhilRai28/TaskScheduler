import pytest
import uuid
from datetime import datetime, timedelta
from typing import Callable, Any

from src.taskscheduler.models import Task, Priority, Status

def target_function(a:int, b:int)->int:
    """A stand-in function for scheduler"""
    return a+b

def test_task_default_value():
    """Verifies initialisation"""

    future_time = datetime.now() + timedelta(minutes=5)

    task = Task(
        title="Default Check",
        scheduled_time=future_time,
        target_function=target_function
    )

    assert task.priority == Priority.MEDIUM
    assert task.status == Status.PENDING

    assert task.args == ()
    assert task.kwargs == {}

    assert task.dependencies == []

    assert task.target_function is target_function

def test_task_unique_id():
    """Ensures the UUID are unique"""

    num_tasks = 100
    task_ids = set()

    for i in range(num_tasks):
        task = Task(
            title=f"Task{i}",
            scheduled_time=datetime.now(),
            target_function=target_function
        )

        task_ids.add(task.task_id)

        assert isinstance(uuid.UUID(task.task_id),uuid.UUID)
    
    assert len(task_ids) == num_tasks

def test_dependecy_not_shared():
    """Checks if dependencies are shared"""

    time = datetime.now()
    task1 = Task(title="t1", scheduled_time=time, target_function=target_function)
    task2 = Task(title="t2", scheduled_time=time, target_function=target_function)

    task1.dependencies.append("AND-I-AM-IRONMAN")

    assert len(task1.dependencies) == 1

    assert task2.dependencies == []
    assert task2.dependencies is not task1.dependencies
