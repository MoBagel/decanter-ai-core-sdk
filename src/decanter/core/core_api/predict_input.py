# pylint: disable=C0103
# pylint: disable=too-many-arguments
# pylint: disable=too-few-public-methods
"""Settings for the PredictResult and PredictTSResult"""
import json

from decanter.core.core_api import CoreBody

import logging

class PredictInput:
    """Predict Input for PredictResult Job.

    Setting test data, best model, and the request body for prediction.

    Attributes:
        data (:class:`~decanter.core.jobs.data_upload.DataUpload`): Test data.
        experiment (:class:`~decanter.core.jobs.experiment.Experiment`):
            Experiment from training.
        pred_body(:class:`~decanter.core.extra.body_obj.PredictBody`):
            Request body for sending predict api.

    Examples:
        .. code-block:: python

            predict_input = PredictInput(data=test_data, experiment=exp,
                                threshold=0.9, keep_columns=['col_1', 'col_3'])

    """
    def __init__(
            self, data, experiment, select_by='by_CVbest', select_model_by='mse', select_model_id='', callback=None,
            keep_columns=None, threshold=None, version=None):
        """
        Init Predict Input

        Args:
            data (:class:`~decanter.core.jobs.data_upload.DataUpload`): Test data.
            experiment (:class:`~decanter.core.jobs.experiment.Experiment`):
                Experiment from training.
            callback (:obj:`str`, optional): A uri to be notified of Decanter Core
                activity state changes.
            keep_columns (:obj:`list`, optional): The names of the columns
                that will be appended to the prediction data.
            threshold (:obj:`double`, optional): Prediction threshold for
                binary classification models. Max = 1, Min = 0
            version (:obj:`int`, optional): Api version
        """
        self.data = data
        self.experiment = experiment
        self.pred_body = CoreBody.PredictBody.create(
            data_id='tmp_data_id', model_id='tmp_model_id', callback=callback,
            keep_columns=keep_columns, threshold=threshold, version=version)
        # '''
        self.select_by = select_by # **
        self.select_model_by = select_model_by # **
        self.select_model_id = select_model_id # **
        # '''

    def getPredictParams(self):
        """Using pred_body to create the JSON request body for prediction.

        Returns:
            :obj:`dict`
        """

        # '''
        if self.select_by == 'by_CVbest':
            print(self.select_by, self.select_model_by, '!!!!!!!!!!!')
            setattr(self.pred_body, 'data_id', self.data.id)
            setattr(self.pred_body, 'model_id', self.experiment.best_model.id)
        # else:
        elif self.select_by == 'by_RC':
            print(self.select_by, self.select_model_by)
            if self.select_model_by in self.experiment.recommend_model_id.keys():
                setattr(self.pred_body, 'data_id', self.data.id)
                setattr(self.pred_body, 'model_id', self.experiment.recommend_model_id[self.select_model_by])
            else:
                logger.error('[%s] no such Metric on model', class_, self.select_model_by) 
        elif self.select_by == 'by_index':
            print(self.select_by, self.select_model_by)
            if self.select_model_id in self.experiment.model_id_list:
                setattr(self.pred_body, 'data_id', self.data.id)
                setattr(self.pred_body, 'model_id', self.select_model_id)
            else:
                logger.error('[%s] no such model ID', class_, self.model_id) 
        # '''

        # setattr(self.pred_body, 'data_id', self.data.id)
        # setattr(self.pred_body, 'model_id', self.experiment.best_model.id)
        params = json.dumps(
            self.pred_body.jsonable(), cls=CoreBody.ComplexEncoder)
        params = json.loads(params)
        return params


class PredictTSInput(PredictInput):
    """Time series predict input for  PredictTSResult Job.

    Setting test data, best model, and the request body for prediction.

    Attributes:
        data (:class:`~decanter.core.jobs.data_upload.DataUpload`): Test data
        experiment (:class:`~decanter.core.jobs.experiment.ExperimentTS`):
            Time series experiment from training.
        pred_body (:class:`~decanter.core.extra.body_obj.PredictTSBody`):
            Request body for sending predict api
    """
    def __init__(
            self, data, experiment, callback=None,
            keep_columns=None, threshold=None, version=None):
        super().__init__(data=data, experiment=experiment)
        self.pred_body = CoreBody.PredictBodyTSModel.create(
            data_id='tmp_data_id', model_id='tmp_model_id', callback=callback,
            keep_columns=keep_columns, threshold=threshold, version=version)
