"""
An enumeration is a set of symbolic names (members)
bound to unique, constant values. Within an enumeration,
the members can be compared by identity, and the enumeration
itself can be iterated over.
"""
from enum import Enum

class Algos(Enum):
    """
    The class Algos are the machined learning algorithms
    currently supported by the Decanter AI Core SDK
    """
    DRF = 'DRF'
    GLM = 'GLM'
    GBM = 'GBM'
    DeepLearning = 'DeepLearning'
    StackedEnsemble = 'StackedEnsemble'
    XGBoost = 'XGBoost'
