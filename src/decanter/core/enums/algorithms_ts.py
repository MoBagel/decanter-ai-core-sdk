"""
Function for user access the Machine Learning
Algorithms of the Decanter AI Core SDK.
"""
from enum import Enum
# list of available models for time series analysis. Future versions will give user more flexibility in specifying
# algorithms of choice
class AlgoTS(Enum):
    """
    The AlgoTS enumeration is the machine learning algorithms currently
    supported by the Decanter AI Core SDK

    - Prophet: Prophet forecasting model for univariate time series datasets
    - Theta: Theta forecasting model
    - DeepLearning: Deep Learning.
    - XGBoost: eXtreme Gradient Boosting.
    """
    prophet = 'Prophet'
    theta = 'Theta'
    DeepLearning = 'DeepLearning'
    XGBoost = 'XGBoost'
