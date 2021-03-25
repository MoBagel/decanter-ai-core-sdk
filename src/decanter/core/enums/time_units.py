'''valid time units that are currently supported by corex'''
from enum import Enum

class TimeUnit(Enum):
    HOUR = 'hour'
    DAY = 'day'
    MONTH = 'month'
    YEAR = 'year'