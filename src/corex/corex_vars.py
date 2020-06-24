# pylint: disable=too-few-public-methods
"""Define variables of corex for all modules."""
from enum import Enum


class CoreXStatus:
    """Status for tasks and jobs."""
    DONE = 'done'
    PENDING = 'pending'
    FAIL = 'fail'
    INVALID = 'invalid'
    RUNNING = 'running'
    DONE_STATUS = [DONE, INVALID, FAIL]
    FAIL_STATUS = [INVALID, FAIL]


class CoreXKeys(Enum):
    """Keys of CoreX responses."""
    id = '_id'
    progress = 'progress'
    status = 'status'
    result = 'result'
