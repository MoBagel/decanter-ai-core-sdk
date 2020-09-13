"""
Function for user access the Metrics 
of the Decanter AI Core SDK.
"""
from enum import Enum

class Evaluator(Enum):
    """
    Evaluator are the metrics currently 
    supported by the Decanter AI Core SDK
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
