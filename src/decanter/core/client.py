# pylint: disable=too-many-arguments
"""Function for user handle the use of Decanter Core API."""
import io
import json
import logging

import pandas as pd

from decanter.core import Context
from decanter.core.jobs import DataUpload,\
                       Experiment, ExperimentTS,\
                       PredictResult, PredictTSResult
import decanter.core.core_api.body_obj as CoreBody

logger = logging.getLogger(__name__)


class CoreClient:
    """Handle client side actions.

    Support actions sunch as setup data, upload data, train,
    predict, time series train and predict...ect.

    Example:
        .. code-block:: python

            from decanter import core
            client = core.CoreClient()
            client.upload(data={csv-file-type/dataframe})

    """
    def __init__(self):
        pass

    @staticmethod
    def setup(
            data_source, data_columns, data_id=None, callback=None,
            eda=None, preprocessing=None, version=None, name=None):
        """Setup data reference.

        Create a DataUpload Job and scheduled the execution in CORO_TASKS list.
        Record the Job in JOBS list.

        Args:
            data_source (dict): Accessor for files in hdfs,{
                    'uri': string-Uri-of-hdfs,
                    'format': Valid dataset format,
                    'opt':(optional)}.
            data_columns (list(dict)): Columns to be used for setup data, list
                of {'id', 'data_type', 'nullable'}.
            data_id (str): ObjectId in 24 hex digit format.
            callback (:obj:`str`, optional): Uri to be notified of decanter
                core activity state changes.
            eda (:obj:`boolen`, optional): Will perform eda on this dataset
                if true.
            preprocessing (:obj:`dict`, optional): Specification for column
                preprocessing.
            version (:obj:`str`, optional): api version
            name (:obj:`str`, optional) string, name for setup action.

        Returns:
            :class:`~decanter.core.jobs.data_upload.DataUpload` object

        Raises:
            AttributeError: If the function is called without
                :class:`~decanter.core.context.Context` created.

        """
        data_columns = CoreBody.column_array(data_columns)
        setup_body = CoreBody.SetupBody.create(
            data_source=data_source,
            data_id=data_id,
            callback=callback,
            eda=eda,
            data_columns=data_columns,
            preprocessing=preprocessing,
            version=version
        )

        params = json.dumps(
            setup_body.jsonable(), cls=CoreBody.ComplexEncoder)
        params = json.loads(params)
        data = DataUpload(setup_params=params, name=name)

        try:
            if Context.LOOP is None:
                raise AttributeError('[Core] event loop is \'NoneType\'')
            task = Context.LOOP.create_task(
                data.wait())
            Context.CORO_TASKS.append(task)
            Context.JOBS.append(data)
        except AttributeError:
            logger.error('[Core] Context not created')
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
            :class:`~decanter.core.jobs.data_upload.DataUpload` object

        Raises:
            AttributeError: If the function is called without
                :class:`~decanter.core.context.Context` created.

        """
        logger.debug('[Core] Create DataUpload Job')

        # check file validation
        if file is None:
            logger.error('[Core] upload file is \'NoneType\'')
            raise Exception
        if isinstance(file, pd.DataFrame):
            file = file.to_csv(index=False)
            file = io.StringIO(file)
            file.name = 'no_name'

        data = DataUpload(file=file, name=name)
        # check context validation
        try:
            if Context.LOOP is None:
                raise AttributeError('[Core] event loop is \'NoneType\'')
            task = Context.LOOP.create_task(data.wait())
            Context.CORO_TASKS.append(task)
            Context.JOBS.append(data)
        except AttributeError:
            logger.error('[Core] Context not created')
            raise
        return data

    @staticmethod
    def train(train_input, select_model_by='mse', name=None):
        """Train model with data.

        Create a Experiment Job and scheduled the execution in CORO_TASKS list.
        Record the Job in JOBS list.

        Args:
            train_input
                (:class:`~decanter.core.core_api.train_input.TrainInput`):
                stores the settings for training.
            name (:obj:`str`, optional): name for train action.

        Returns:
            :class:`~decanter.core.jobs.experiment.Experiment` object

        Raises:
            AttributeError: If the function is called without
                :class:`~decanter.core.context.Context` created.
        """
        logger.debug('[Core] Create Train Job')
        exp = Experiment(
            train_input=train_input,
            select_model_by=select_model_by, name=name)
        try:
            if Context.LOOP is None:
                raise AttributeError('[Core] event loop is \'NoneType\'')
            task = Context.LOOP.create_task(exp.wait())
            Context.CORO_TASKS.append(task)
            Context.JOBS.append(exp)
        except AttributeError:
            logger.error('[Core] Context not created')
            raise
        return exp

    @staticmethod
    def train_ts(train_input, select_model_by='mse', name=None):
        """Train time series model with data.

        Create a Time Series Experiment Job and scheduled the execution
        in CORO_TASKS list.  Record the Job in JOBS list.

        Args:
            train_input
                (:class:`~decanter.core.core_api.train_input.TrainTSInput`):
                Settings for training.
            name (:obj:`str`, optional): name for train time series action.

        Returns:
            :class:`~decanter.core.jobs.experiment.ExperimentTS` object

        Raises:
            AttributeError: If the function is called without
                :class:`~decanter.core.context.Context` created.
        """
        logger.debug('[Core] Create Train Job')
        exp_ts = ExperimentTS(
            train_input=train_input,
            select_model_by=select_model_by,
            name=name)
        try:
            if Context.LOOP is None:
                raise AttributeError('[Core] event loop is \'NoneType\'')
            task = Context.LOOP.create_task(exp_ts.wait())
            Context.CORO_TASKS.append(task)
            Context.JOBS.append(exp_ts)
        except AttributeError:
            logger.error('[Core] Context not created')
            raise
        return exp_ts

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
            :class:`~decanter.core.jobs.predict_result.PredictResult` object

        Raises:
            AttributeError: If the function is called without
                :class:`~decanter.core.context.Context` created

        """
        logger.debug('[Core] Create Predict Job')
        predict_res = PredictResult(predict_input=predict_input, name=name)
        try:
            if Context.LOOP is None:
                raise AttributeError('[Core] event loop is \'NoneType\'')
            task = Context.LOOP.create_task(predict_res.wait())
            Context.CORO_TASKS.append(task)
            Context.JOBS.append(predict_res)
        except AttributeError:
            logger.error('[Core] Context not created')
            raise
        return predict_res

    @staticmethod
    def predict_ts(predict_input, name=None):
        """Predict time series model with test data.

        Create a Time Series PredictResult Job and scheduled the execution
        in CORO_TASKS list.  Record the Job in JOBS list.

        Args:
            predict_input
                (:class:`~decanter.core.core_api.predict_input.PredictTSInput`):
                stores the settings for prediction.
            name (:obj:`str`, optional): name for predict time series action.

        Returns:
            :class:`~decanter.core.jobs.predict_result.PredictTSResult`
            object.

        Raises:
            AttributeError: If the function is called without
                :class:`~decanter.core.context.Context` created
        """
        logger.debug('[Core] Create Predict Job')
        predict_ts_res = PredictTSResult(
            predict_input=predict_input, name=name)
        try:
            if Context.LOOP is None:
                raise AttributeError('[Core] event loop is \'NoneType\'')
            task = Context.LOOP.create_task(predict_ts_res.wait())
            Context.CORO_TASKS.append(task)
            Context.JOBS.append(predict_ts_res)
        except AttributeError:
            logger.error('[Core] Context not created')
            raise

        return predict_ts_res
