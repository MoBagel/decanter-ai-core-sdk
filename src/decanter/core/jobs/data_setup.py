# pylint: disable=C0103
# pylint: disable=too-many-instance-attributes
"""DataSetup

Handle data setup to Decanter Core server Stores Data
attribute.

"""
import io
import logging

import pandas as pd

from decanter.core.extra import CoreStatus
from decanter.core.extra.decorators import update
from decanter.core.extra.utils import check_response, gen_id
from decanter.core.jobs.job import Job
from decanter.core.jobs.data_upload import DataUpload
from decanter.core.jobs.task import SetupTask


logger = logging.getLogger(__name__)


class DataSetup(DataUpload, Job):
    """DataSetup manage to get the result from data setup.

    Handle the execution of setup task in order to setup data to
    Decanter Core server Stores the setup results in DataSetup attributes.

    Attributes:
        jobs (list): None, list up jobs that DataSetup needs to wait for.
        task (:class:`~decanter.core.jobs.task.SetupTask`): Setup task run by
            DataSetup.
        accessor (dict): Accessor for files in hdfs.
        schema (dict): The original data schema.
        originSchema (dict): The original data schema.
        annotationsMeta (dict): information: Extra information for data.
        options (dict): Extra information for data.
        created_at (str): The date the data was created.
        updated_at (str): The time the data was last updated.
        completed_at (str): The time the data was completed at.
        name (str): Name to track Job progress, will give default name if None.
    """
    def __init__(self, train_data=None, setup_params=None, name=None):
        """DataSetup Init.

        Args:
            train_data (:obj:`~decanter.core.jobs.data_setup.DataSetup)
            setup_params (:obj:`dict`, optional): Settings for setup data.
            name (:obj:`str`, optional): Name to track Job progress
        """
        Job.__init__(
            self,
            jobs=[train_data],
            task=SetupTask(setup_params, name),
            name=gen_id(self.__class__.__name__, name))
        self.accessor = None
        self.schema = None
        self.originSchema = None
        self.annotations = None
        self.options = None
        self.created_at = None
        self.updated_at = None
        self.completed_at = None
