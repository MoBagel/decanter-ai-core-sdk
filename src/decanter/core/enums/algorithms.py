"""
Function for user access the Machine Learning
Algorithms of the Decanter AI Core SDK.
"""
from enum import Enum

class Algo(Enum):
    """
    The Algo enumeration is the machine learning algorithms currently 
    supported by the Decanter AI Core SDK

    - DRF: Distributed Random Forest.  
    - GLM: Generalized Linear Model.
    - GBM: Gradient Boosting Machine.
    - DeepLearning: Deep Learning.
    - StackedEnsemble: Stacked Ensemble.
    - XGBoost: eXtreme Gradient Boosting.
    """
    DRF = 'DRF'
    GLM = 'GLM'
    GBM = 'GBM'
    DeepLearning = 'DeepLearning'
    StackedEnsemble = 'StackedEnsemble'
    XGBoost = 'XGBoost'
