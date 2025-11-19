from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable, Any
import uuid

from . import Priority,Status

@dataclass
class Task:
    """Represents a scheduled unit of work"""

    target_function: Callable[[Any],Any]
    title: str
    scheduled_time: datetime

    task_id: str = field(default_factory=lambda: str(uuid.uuid4()), init=False)

    priority: Priority = Priority.MEDIUM
    status: Status = Status.PENDING

    args: tuple = field(default_factory=tuple)
    kwargs: tuple = field(default_factory=dict)

    dependencies: list[str] = field(default_factory=list)

    reccuring_interval: Any = None