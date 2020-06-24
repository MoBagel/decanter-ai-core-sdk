# pylint: disable=C0103
# pylint: disable=too-many-arguments
# pylint: disable=too-few-public-methods
"""Settings for the PredictResult and PredictTSResult

  Typical usage example:

  predict_input = PredictInput(data=test_data, experiment=exp,
                    threshold=0.9, keep_columns=['col_1', 'col_3'])
"""
import json

import corex.extra.corex_objs as CoreXOBJ


class PredictInput:
    """Predict Input for PredictResult Job.

    Setting test data, best model, and the request body for prediction.

    Attributes:
        data(class:`DataUpload <Job>`): Test data
        experiment(class:`Experiment <Job>`): Experiment from training
        pred_body(class `PredictBody <CoreXOBJ>`):
            Request body for sending predict api
    """
    def __init__(
            self, data, experiment, callback=None,
            keep_columns=None, threshold=None, version=None):
        """Init Predict Input

        Args:
            data(class:`DataUpload <Job>`): Test data
            experiment(class:`Experiment <Job>`): Experiment from training
            callback(str): A uri to be notified of corex activity state changes
            keep_columns(lst): The names of the columns that will be appended
                to the prediction data
            threshold(double): Prediction threshold for binary classification
                models. Max = 1, Min = 0
            version(int): Api version
        """
        self.data = data
        self.experiment = experiment
        self.pred_body = CoreXOBJ.PredictBody.create(
            data_id='tmp_data_id', model_id='tmp_model_id', callback=callback,
            keep_columns=keep_columns, threshold=threshold, version=version)

    def getPredictParams(self):
        """Using pred_body to create the JSON request body for prediction.

        Returns:
            JSON Python object
        """
        setattr(self.pred_body, 'data_id', self.data.id)
        setattr(self.pred_body, 'model_id', self.experiment.best_model.id)
        params = json.dumps(
            self.pred_body.jsonable(), cls=CoreXOBJ.ComplexEncoder)
        params = json.loads(params)
        return params


class PredictTSInput(PredictInput):
    """Time series predict input for  PredictTSResult Job.

    Setting test data, best model, and the request body for prediction.

    Attributes:
        data(class:`DataUpload <Job>`): Test data
        experiment(class:`Experiment <Job>`): Experiment from training
        pred_body(class `PredictBody <CoreXOBJ>`):
            Request body for sending predict api
    """
    def __init__(
            self, data, experiment, callback=None,
            keep_columns=None, threshold=None, version=None):
        super().__init__(data=data, experiment=experiment)
        self.pred_body = CoreXOBJ.PredictBodyTSModel.create(
            data_id='tmp_data_id', model_id='tmp_model_id', callback=callback,
            keep_columns=keep_columns, threshold=threshold, version=version)
