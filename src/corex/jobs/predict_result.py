# pylint: disable=invalid-name
# pylint: disable=too-many-instance-attributes
# pylint: disable=super-init-not-called
"""Experiment and ExperimentTS

Handle model training on corex server. Stores Experiment results
in attribute.
"""
import io
import logging

import pandas as pd

from corex.extra.decorators import update
from corex.jobs.job import Job
from corex.jobs.task import PredictTask, PredictTSTask
from corex.extra.utils import check_response, gen_id


logger = logging.getLogger(__name__)


class PredictResult(Job):
    """PredictResult

    Handle Prediction on corex server. Stores Predict Result to
    attribute.

    Attributes:
        jobs (lst): None, list up jobs that PredictResult needs to wait for.
        task (class:`PredictTask <CoreXTask>`):
            upload task run by PredictResult job
        accessor (JSON): Accessor for files in hdfs
        schema (JSON): The original data schema
        originSchema (JSON): The original data schema
        annotationsMeta (JSON): information: Extra information for data
        options (JSON): Extra information for data
        created_at (str): The date the data was created
        updated_at (str): The time the data was last updated
        completed_at (str): The time the data was completed at
    """
    def __init__(self, predict_input, name=None):
        super().__init__(
            jobs=[predict_input.data, predict_input.experiment],
            task=PredictTask(predict_input, name=name),
            name=gen_id('PredResult', name))
        self.accessor = None
        self.schema = None
        self.originSchema = None
        self.annotations = None
        self.options = None
        self.created_at = None
        self.updated_at = None
        self.completed_at = None

    @update
    def update_result(self, task_result):
        """Update Job's attribute from Task's result."""
        return

    def show(self):
        """Show content of predict result.

        Returns:
            str (content of PredictResult)
        """
        pred_txt = ''
        if self.is_success():
            pred_txt = check_response(
                self.core_service.get_data_file_by_id(self.id)).text
        else:
            logger.error('[%s] fail', self.__class__.__name__)
        return pred_txt

    def show_df(self):
        """Show predict result in pandas dataframe.

        Returns:
            class pandas.DataFrame
        """
        pred_df = None
        if self.is_success():
            pred_csv = check_response(
                self.core_service.get_data_file_by_id(self.id))
            pred_csv = pred_csv.content.decode('utf-8')
            pred_df = pd.read_csv(io.StringIO(pred_csv))
        else:
            logger.error('[%s] fail', self.__class__.__name__)
        return pred_df

    def download_csv(self, path):
        """DownLoad csv format of the predict result."""
        if self.is_success():
            data_csv = check_response(
                self.core_service.get_data_file_by_id(self.id)).text
            save_csv = open(path, 'w+')
            save_csv.write(data_csv)
            save_csv.close()
        else:
            logger.error('[%s] Fail to Download', self.__class__.__name__)


class PredictTSResult(PredictResult, Job):
    """Predict time series's model result.

    Handle time series's model Prediction on corex server.  Stores
    predict Result to attribute.

    Attributes:
        jobs(lst): None, list up jobs that PredictTSResult needs to wait for.
        task(class:`PredictTSTask <CoreXTask>`):
            upload task run by PredictResult job
        accessor(JSON): Accessor for files in hdfs
        schema(JSON): The original data schema
        originSchema(JSON): The original data schema
        annotationsMeta(JSON): information: Extra information for data
        options(JSON): Extra information for data
        created_at(str): The date the data was created
        updated_at(str): The time the data was last updated
        completed_at(str): The time the data was completed at
    """
    def __init__(self, predict_input, name=None):
        Job.__init__(
            self,
            jobs=[predict_input.data, predict_input.experiment],
            task=PredictTSTask(predict_input, name=name),
            name=gen_id('PredTSResult', name))
        self.accessor = None
        self.schema = None
        self.originSchema = None
        self.annotations = None
        self.options = None
        self.created_at = None
        self.updated_at = None
        self.completed_at = None
