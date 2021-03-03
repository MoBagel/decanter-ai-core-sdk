# pylint: disable=too-many-arguments
"""Function for user handle the use of Decanter GP API."""
import io
import json
import logging
import requests

import pandas as pd

from decanter.core import Context
from decanter.core.jobs import GPDataUpload, GPDataSetup,\
                       GPExperiment, \
                       GPPredictResult
import decanter.core.core_api.body_obj as CoreBody
from decanter.core.enums.evaluators import Evaluator
from decanter.core.enums import check_is_enum
import decanter.core.jobs.task as jobsTask

logger = logging.getLogger(__name__)


class GPClient(Context):
    """Handle client side actions.

    Support actions sunch as setup data, upload data, train,
    predict, time series train and predict...ect.

    Example:
        .. code-block:: python

            from decanter import core
            client = core.GPlient()
            client.upload(data={csv-file-type/dataframe})

    """
    def __init__(self, apikey, host):
        """Create context instance and init neccessary variable and objects.

            Setting the user, password, and host for the funture connection when
            calling APIs, and create an event loop if it isn't exist. Check if the
            connection is healthy after args be set.

        Args:
            apikey (str): apikey for logging into Decanter GP server
            host (str): Decanter GP server URL.
        """
        Context.create(apikey=apikey, host=host)
        self.healthy()

    @staticmethod
    def healthy():
        """Check the connection between Decanter GP server.

        Send a fake request to determine if there's connection or
        authorization errors.

        """
        try:
            res = requests.get(Context.HOST)
            if res.status_code // 100 != 2:
                raise Exception()
        except Exception as err:
            logger.error('[Context] connect not healthy :(')
            raise SystemExit(err)
        else:
            logger.info('[Context] connect healthy :)')

    @staticmethod
    def setup(setup_input, name=None):
        """Setup data reference.

        Create a DataSetup Job and scheduled the execution in CORO_TASKS list.
        Record the Job in JOBS list.

        Args:
            setup_input
                (:class:`~decanter.core.core_api.setup_input.GPSetupInput`):
                stores the settings for training.
            name (:obj:`str`, optional): name for setup action.

        Returns:
            :class:`~decanter.core.jobs.data_setup.DataSetup` object

        Raises:
            AttributeError: If the function is called without
                :class:`~decanter.core.context.Context` created.

        """

        data = GPDataSetup(setup_input=setup_input, name=name)

        try:
            if Context.LOOP is None:
                raise AttributeError('[GP] event loop is \'NoneType\'')
            task = Context.LOOP.create_task(
                data.wait())
            Context.CORO_TASKS.append(task)
            Context.JOBS.append(data)
        except AttributeError:
            logger.error('[GP] Context not created')
            raise
        return data

    @staticmethod
    def upload(file, name=None):
        """Upload csv file or pandas dataframe.

        Create a DataUpload Job and scheduled the execution in CORO_TASKS list.
        Record the Job in JOBS list.

        Args:
            file (csv-file, :obj:`pandas.DataFrame`): File uploaded to
                core server.
            name (:obj:`str`, optional): Name for upload action.

        Returns:
            :class:`~decanter.core.jobs.data_upload.GPDataUpload` object

        Raises:
            AttributeError: If the function is called without
                :class:`~decanter.core.context.Context` created.

        """
        logger.debug('[GP] Create DataUpload Job')

        # check file validation
        if file is None:
            logger.error('[GP] upload file is \'NoneType\'')
            raise Exception
        if isinstance(file, pd.DataFrame):
            file = file.to_csv(index=False)
            file = io.StringIO(file)
            file.name = 'no_name'

        data = GPDataUpload(file=file, name=name)
        # check context validation
        try:
            if Context.LOOP is None:
                raise AttributeError('[GP] event loop is \'NoneType\'')
            task = Context.LOOP.create_task(data.wait())
            Context.CORO_TASKS.append(task)
            Context.JOBS.append(data)
        except AttributeError:
            logger.error('[GP] Context not created')
            raise
        return data

    @staticmethod
    def train(train_input, select_model_by=Evaluator.auto, name=None):
        """Train model with data.

        Create a Experiment Job and scheduled the execution in CORO_TASKS list.
        Record the Job in JOBS list.

        Args:
            train_input
                (:class:`~decanter.core.core_api.train_input.TrainInput`):
                stores the settings for training.
            name (:obj:`str`, optional): name for train action.

        Returns:
            :class:`~decanter.core.jobs.experiment.GPExperiment` object

        Raises:
            AttributeError: If the function is called without
                :class:`~decanter.core.context.Context` created.
        """
        select_model_by = check_is_enum(Evaluator, select_model_by)
        logger.debug('[GP] Create Train Job')
        exp = GPExperiment(
                train_input=train_input,
                select_model_by=select_model_by, name=name)
        try:
            if Context.LOOP is None:
                raise AttributeError('[GP] event loop is \'NoneType\'')
            task = Context.LOOP.create_task(exp.wait())
            Context.CORO_TASKS.append(task)
            Context.JOBS.append(exp)
        except AttributeError:
            logger.error('[GP] Context not created')
            raise
        return exp

    @staticmethod
    def predict(predict_input, name=None):
        """Predict model with test data.

        Create a PredictResult Job and scheduled the execution
        in CORO_TASKS list. Record the Job in JOBS list.

        Args:
            predict_input
                (:class:`~decanter.core.core_api.predict_input.PredictInput`):
                stores the settings for prediction.
            name (:obj:`str`, optional): string, name for predict action.

        Returns:
            :class:`~decanter.core.jobs.predict_result.GPPredictResult` object

        Raises:
            AttributeError: If the function is called without
                :class:`~decanter.core.context.Context` created

        """
        logger.debug('[GP] Create Predict Job')
        predict_res = GPPredictResult(predict_input=predict_input, name=name)
        try:
            if Context.LOOP is None:
                raise AttributeError('[GP] event loop is \'NoneType\'')
            task = Context.LOOP.create_task(predict_res.wait())
            Context.CORO_TASKS.append(task)
            Context.JOBS.append(predict_res)
        except AttributeError:
            logger.error('[GP] Context not created')
            raise
        return predict_res

