"""
The enumerate Algos are the machined learning algorithms
currently supported by the Decanter AI Core SDK
"""
from enum import Enum

class Algos(Enum):
    DRF = 'DRF'
    GLM = 'GLM'
    GBM = 'GBM'
    DeepLearning = 'DeepLearning'
    StackedEnsemble = 'StackedEnsemble'
    XGBoost = 'XGBoost'
