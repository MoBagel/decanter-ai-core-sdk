# pylint: disable=too-many-arguments
"""Client side function for user using CoreX API.

  Typical usage example:

  corex = CoreXAPI()
  corex.upload(data={csv-file-type/dataframe})
"""
import io
import json
import logging

import pandas as pd

from corex import Context
from corex.jobs import DataUpload, Experiment, ExperimentTS, PredictResult, PredictTSResult
import corex.extra.corex_objs as CoreXOBJ

logger = logging.getLogger(__name__)


class CoreXAPI:
    """Handle client side actions.

    Support actions sunch as setup data, upload data, train,
    predict, time series train and predict...ect.
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
            data_source: JSON object, {
                    'uri': string-Uri-of-hdfs, 'format': Valid dataset format,
                    'opt':(opt)}
            data_columns: list of {'id', 'data_type', 'nullable'},
                    Columns to be used for setup data.
            data_id: string, ObjectId in 24 hex digit format
            callback: (opt) uri to be notified of corex activity state changes
            eda: (opt) boolen, will perform eda on this dataset if true
            preprocessing: (opt) list, specification for column preprocessing
            version: (opt) string, api version
            name: (opt) string, name for setup action.

        Returns:
            class:`DataUpload <Job>` object

        Raises:
            AttributeError: Call the function without create context.

        """
        data_columns = CoreXOBJ.column_array(data_columns)
        setup_body = CoreXOBJ.SetupBody.create(
            data_source=data_source,
            data_id=data_id,
            callback=callback,
            eda=eda,
            data_columns=data_columns,
            preprocessing=preprocessing,
            version=version
        )

        params = json.dumps(
            setup_body.jsonable(), cls=CoreXOBJ.ComplexEncoder)
        params = json.loads(params)
        data = DataUpload(setup_params=params, name=name)

        try:
            if Context.LOOP is None:
                raise AttributeError('[CoreX] event loop is \'NoneType\'')
            task = Context.LOOP.create_task(
                data.wait())
            Context.CORO_TASKS.append(task)
            Context.JOBS.append(data)
        except AttributeError:
            logger.error('[CoreX] Context not created')
            raise
        return data

    @staticmethod
    def upload(file, name=None):
        """Upload csv file or pandas dataframe.

        Create a DataUpload Job and scheduled the execution in CORO_TASKS list.
        Record the Job in JOBS list.

        Args:
            file: csv-file-object or dataframe, file to upload to corex server.
            name: (opt) string, name for upload action.

        Returns:
            class:`DataUpload <Job>` object

        Raises:
            AttributeError: Call the function without create context.
        """
        logger.debug('[CoreX] Create DataUpload Job')

        # check file validation
        if file is None:
            logger.error('[CoreX] upload file is \'NoneType\'')
            raise Exception
        if isinstance(file, pd.DataFrame):
            file = file.to_csv(index=False)
            file = io.StringIO(file)
            file.name = 'no_name'

        data = DataUpload(file=file, name=name)
        # check context validation
        try:
            if Context.LOOP is None:
                raise AttributeError('[CoreX] event loop is \'NoneType\'')
            task = Context.LOOP.create_task(data.wait())
            Context.CORO_TASKS.append(task)
            Context.JOBS.append(data)
        except AttributeError:
            logger.error('[CoreX] Context not created')
            raise
        return data

    @staticmethod
    def train(train_input, select_model_by='mse', name=None):
        """Train model with data.

        Create a Experiment Job and scheduled the execution in CORO_TASKS list.
        Record the Job in JOBS list.

        Args:
            train_input: class:`TrainInput <TrainInput>`,
                    stores the settings for training.
            name: (opt) string, name for train action.

        Returns:
            class:`Experiment <Job>` object

        Raises:
            AttributeError: Call the function without create context.
        """
        logger.debug('[CoreX] Create Train Job')
        exp = Experiment(
            train_input=train_input,
            select_model_by=select_model_by, name=name)
        try:
            if Context.LOOP is None:
                raise AttributeError('[CoreX] event loop is \'NoneType\'')
            task = Context.LOOP.create_task(exp.wait())
            Context.CORO_TASKS.append(task)
            Context.JOBS.append(exp)
        except AttributeError:
            logger.error('[CoreX] Context not created')
            raise
        return exp

    @staticmethod
    def train_ts(train_input, select_model_by='mse', name=None):
        """Train time series model with data.

        Create a Time Series Experiment Job and scheduled the execution
        in CORO_TASKS list.  Record the Job in JOBS list.

        Args:
            train_input: class:`TrainTSInput <TrainTSInput>`,
                    stores the settings for training.
            name: (opt) string, name for train action.

        Returns:
            class:`ExperimentTS <Job>` object

        Raises:
            AttributeError: Call the function without create context.
        """
        logger.debug('[CoreX] Create Train Job')
        exp_ts = ExperimentTS(
            train_input=train_input,
            select_model_by=select_model_by,
            name=name)
        try:
            if Context.LOOP is None:
                raise AttributeError('[CoreX] event loop is \'NoneType\'')
            task = Context.LOOP.create_task(exp_ts.wait())
            Context.CORO_TASKS.append(task)
            Context.JOBS.append(exp_ts)
        except AttributeError:
            logger.error('[CoreX] Context not created')
            raise
        return exp_ts

    @staticmethod
    def predict(predict_input, name=None):
        """Predict model with test data.

        Create a PredictResult Job and scheduled the execution
        in CORO_TASKS list. Record the Job in JOBS list.

        Args:
            predict_input: class:`PredictInput <PredictInput>`,
                    stores the settings for prediction.
            name: (opt) string, name for predict action.

        Returns:
            class:`PredictResult <Job>` object

        Raises:
            AttributeError: Call the function without create context.
        """
        logger.debug('[CoreX] Create Predict Job')
        predict_res = PredictResult(predict_input=predict_input, name=name)
        try:
            if Context.LOOP is None:
                raise AttributeError('[CoreX] event loop is \'NoneType\'')
            task = Context.LOOP.create_task(predict_res.wait())
            Context.CORO_TASKS.append(task)
            Context.JOBS.append(predict_res)
        except AttributeError:
            logger.error('[CoreX] Context not created')
            raise
        return predict_res

    @staticmethod
    def predict_ts(predict_input, name=None):
        """Predict time series model with test data.

        Create a Time Series PredictResult Job and scheduled the execution
        in CORO_TASKS list.  Record the Job in JOBS list.

        Args:
            train_input: class:`PredictTSResult <PredictTSResult>`,
                    stores the settings for prediction.
            name: (opt) string, name for train action.

        Returns:
            class:`PredictTSResult <Job>` object

        Raises:
            AttributeError: Call the function without create context.
        """
        logger.debug('[CoreX] Create Predict Job')
        predict_ts_res = PredictTSResult(
            predict_input=predict_input, name=name)
        try:
            if Context.LOOP is None:
                raise AttributeError('[CoreX] event loop is \'NoneType\'')
            task = Context.LOOP.create_task(predict_ts_res.wait())
            Context.CORO_TASKS.append(task)
            Context.JOBS.append(predict_ts_res)
        except AttributeError:
            logger.error('[CoreX] Context not created')
            raise

        return predict_ts_res
