"""
Function for user access the Evaluators Metrics 
of the Decanter AI Core SDK.
"""
from enum import Enum

class Evaluator(Enum):
    """
    The Evaluator enumeration is the metrics currently 
    supported by the Decanter AI Core SDK
    
    - Regression
        - auto (deviance)
        - deviance
        - mse
        - mae
        - rmsle
        - r2
    - Binary Classification
        - auto (logloss)
        - logloss
        - lift_top_group
        - auc
        - misclassification
    - Multinomial Classification
        - auto (logloss)
        - logloss
        - misclassification
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
