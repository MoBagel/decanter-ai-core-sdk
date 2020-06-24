# pylint: disable=C0103
# pylint: disable=too-many-instance-attributes
"""DataUpload

Handle data upload to corex server. Stores Data
attribute.

    Typical usage example:

    data = DataUpload.create({data_id})
    data.show_df()
"""
import io
import logging

import pandas as pd

from corex.corex_vars import CoreXStatus
from corex.extra.decorators import update
from corex.extra.utils import check_response, gen_id
from corex.jobs.job import Job
from corex.jobs.task import UploodTask, SetupTask


logger = logging.getLogger(__name__)


class DataUpload(Job):
    """DataUpload manage to get the result from data upload.

    Handle the execution of upload task in order to upload data to
    coreX server. Stores the upload results in DataUpload attributes.

    Attributes:
        jobs(lst): None, list up jobs that DataUpload needs to wait for.
        task(class:`UploodTask <CoreXTask>`):
            upload task run by DataUpload job
        accessor(JSON): Accessor for files in hdfs
        schema(JSON): The original data schema
        originSchema(JSON): The original data schema
        annotationsMeta(JSON): information: Extra information for data
        options(JSON): Extra information for data
        created_at(str): The date the data was created
        updated_at(str): The time the data was last updated
        completed_at(str): The time the data was completed at
        name(str): Name to track Job progress
    """
    def __init__(self, file=None, setup_params=None, name=None):
        """DataUpload Init.

        Args:
            file(file-object): DataUpload file to upload
            setup_params(JSON): (opt)
            name(str): Name to track Job progress
        """
        super().__init__(jobs=None,
                         task=(UploodTask(file, name)
                               if file is not None
                               else SetupTask(setup_params, name)),
                         name=gen_id(self.__class__.__name__, name))

        self.accessor = None
        self.schema = None
        self.originSchema = None
        self.annotations = None
        self.options = None
        self.created_at = None
        self.updated_at = None
        self.completed_at = None

    @classmethod
    def create(cls, data_id, name=None):
        """Create data by data_id.

        Args:
            data_id(str): ObjectId in 24 hex digits
            name(str): (opt) Name to track Job progress

        Returns:
            class:`DataUpload <Job>` object
        """
        data = cls()
        data_resp = check_response(
            data.core_service.get_data_by_id(data_id)).json()
        data.update_result(data_resp)
        data.status = CoreXStatus.DONE
        data.name = name
        return data

    @update
    def update_result(self, task_result):
        """Update from 'result' in Task response."""
        return

    def show(self):
        """Show data content.

        Returns:
            str (content of DataUpload)
        """
        data_txt = None
        if self.is_success():
            data_txt = check_response(
                self.core_service.get_data_file_by_id(self.id)).text
        else:
            logger.error(
                '[%s] \'%s\' show data failed',
                self.__class__.__name__, self.name)
        return data_txt

    def show_df(self):
        """Show data in pandas dataframe.

        Returns:
            class pandas.DataFrame
        """
        data_df = None
        if self.is_success():
            data_csv = check_response(
                self.core_service.get_data_file_by_id(self.id))
            data_csv = data_csv.content.decode('utf-8')
            data_df = pd.read_csv(io.StringIO(data_csv))
        else:
            logger.error('[%s get result] fail', self.__class__.__name__)
        return data_df

    def download_csv(self, path):
        """DownLoad csv format of the predict result."""
        if self.is_success():
            data_csv = check_response(
                self.core_service.get_data_file_by_id(self.id)).text
            save_csv = open(path, 'w+')
            save_csv.write(data_csv)
            save_csv.close()
        else:
            logger.error('[%s get result] fail', self.__class__.__name__)
