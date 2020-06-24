"""Mobagel CoreX Python SDK

mobagel-corex is a python library for the easy use of CoreX APIs.

"""
import logging
import sys

from .context import Context
from .corex_api import CoreXAPI
from .model import Model, MultiModel
from .predict_input import PredictInput, PredictTSInput
from .train_input import TrainInput, TrainTSInput


corex_logger = logging.getLogger(__name__)
corex_logger.addHandler(logging.NullHandler())


def enable_default_logger():
    """Set the default logger handler for corex.

    Will set the root handles to empty list, prevent duplicate handlers added
    by other packages causing duplicate logging message.
    """
    logging.root.handlers = []

    if all(isinstance(handler, logging.NullHandler)
           for handler in corex_logger.handlers):

        corex_logger.setLevel(logging.INFO)
        default_handler = logging.StreamHandler(sys.stderr)
        default_handler.setFormatter(
            logging.Formatter(
                fmt='%(asctime)s [%(levelname)8s] '
                    '%(message)s (%(filename)s:%(lineno)s)',
                datefmt='%H:%M:%S')
        )
        corex_logger.addHandler(default_handler)
