"""Class for accessing Decanter GP Backend (BE)"""
import io
import logging
import pandas as pd

from decanter.gp import Context

logger = logging.getLogger(__name__)


class GPClient(Context):
    """Handle client side operations.

    Support actions such as:
        - (TODO) Upload
        - (TODO) Train
        - (TODO) Predict
        - (TODO) etc

    Example:
    TODO: describe usage of the GP Client
    """

    def __init__(self, username: str, password: str, host: str, )
