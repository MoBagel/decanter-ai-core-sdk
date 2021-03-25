'''available numerical group by methods supported by corex'''
import enum as Enum

class NumericalGroupByMethod(Enum):
    SUM = 'sum'
    MEAN = 'mean'
    COUNT = 'count'