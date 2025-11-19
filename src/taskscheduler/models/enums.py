from enum import Enum

class Priority(Enum):
    """Defines the importance level of a task"""
    HIGH    = 3
    MEDIUM  = 2
    LOW     = 1

class Status(Enum):
    """Defines the status of the current task"""
    PENDING = 'PENDING'
    RUNNING = 'RUNNING'
    SUCCESS = 'SUCCESS'
    FAILED  = 'FAILED'