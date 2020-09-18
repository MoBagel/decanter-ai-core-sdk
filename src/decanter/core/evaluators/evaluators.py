"""
An enumeration is a set of symbolic names (members)
bound to unique, constant values. Within an enumeration,
the members can be compared by identity, and the enumeration
itself can be iterated over.
"""
from enum import Enum

class Evaluator(Enum):
    """
    the class Evaluator are the metrics
    currently supported by the Decanter AI Core SDK
    """
    auto = 'auto'
    mse = 'mse'
    rmse = 'rmse'
    mae = 'mae'
    rmsle = 'rmsle'
    auc = 'auc'
    logloss = 'logloss'
    deviance = 'deviance'
    r2 = 'r2'
    lift_top_group = 'lift_top_group'
    misclassification = 'misclassification'
    mean_per_class_error = 'mean_per_class_error'
