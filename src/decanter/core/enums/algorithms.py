"""
Function for user access the Machine Learning
Algorithms of the Decanter AI Core SDK.
"""
from enum import Enum

class Algo(Enum):
    """
    The Algo enumeration is the machine learning algorithms currently 
    supported by the Decanter AI Core SDK

    TrainInput (used by client.train) supported algorithms

    - DRF: Distributed Random Forest.  
    - GLM: Generalized Linear Model.
    - GBM: Gradient Boosting Machine.
    - DeepLearning: Deep Learning.
    - StackedEnsemble: Stacked Ensemble.
    - XGBoost: eXtreme Gradient Boosting.

    TrainTSInput (used by client.train_ts) supported algorithms

    - GLM: Generalized Linear Model.
    - DRF: Distributed Random Forest.
    - GBM: Gradient Boosting Machine.
    - XGBoost: eXtreme Gradient Boosting.
    - arima: auto arima (available only after 4.9 deployed with Exodus, only available for regression).
    - prophet: auto arima (available only after 4.9 deployed with Exodus, only available for regression).
    - ets: auto arima (available only after 4.9 deployed with Exodus, only available for regression).
    """
    DRF = 'DRF'
    GLM = 'GLM'
    GBM = 'GBM'
    DeepLearning = 'DeepLearning'
    StackedEnsemble = 'StackedEnsemble'
    XGBoost = 'XGBoost'
    arima = 'arima'
    prophet = 'prophet'
    ets = 'ets'
