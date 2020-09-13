"""
Function for user access the Algorithms
of the Decanter AI Core SDK.
"""
from enum import Enum

class Algos(Enum):
    """
    Evaluator are the algorithms currently 
    supported by the Decanter AI Core SDK
    """
    DRF = 'DRF'
    GLM = 'GLM'
    GBM = 'GBM'
    DeepLearning = 'DeepLearning'
    StackedEnsemble = 'StackedEnsemble'
    XGBoost = 'XGBoost'
