# pylint: disable=too-many-instance-attributes
# pylint: disable=super-init-not-called
"""Experiment and ExperimentTS

Handle model training on corex server. Stores Experiment results
in attribute.

"""
import logging

from corex.core import CoreService
from corex.corex_vars import CoreXStatus
from corex.extra.decorators import update
from corex.extra.utils import check_response, gen_id
from corex.jobs.job import Job
from corex.jobs.task import TrainTask, TrainTSTask
from corex.model import Model, MultiModel


logger = logging.getLogger(__name__)


class Experiment(Job):
    """Experiment manage to get the result from model training.

    Handle the execution of training task in order train model on
    coreX server. Stores the training results in Experiment's attributes.

    Attributes:
        jobs(lst): [DataUpload]. List of jobs that Experiment needs to wait
            till completed
        task(class:`TrainTask <CoreXTask>`):
            Train task run by Experiment Job
        train_input(class:`TrainInput <TrainInput>`):
            Settings for training models
        best_model(class:`Model <Model>`): Model with the best score in
            `select_model_by` argument
        select_model_by(str): the score to select best model
        features(lst): The features used for training
        train_data_id(str): The ID of the train data
        target(str): The target of the experiment
        test_base_id(str): The ID for the test base data
        models(lst): The models' id of the experiment
        hyperparameters(JSON): The hyperparameters of the experiment
        attributes(JSON): The experiment attributes
        recommendations(JSON): Recommended model for each evaluator.
        created_at(str): The date the data was created
        options(JSON): Extra information for experiment
        updated_at(str): The time the data was last updated
        completed_at(str): The time the data was completed at
        name(str): Name to track Job progress
    """
    def __init__(self, train_input, select_model_by='mse', name=None):
        super().__init__(
            jobs=[train_input.data],
            task=TrainTask(train_input, name=name),
            name=gen_id('Exp', name))

        self.train_input = train_input
        self.best_model = Model()
        self.select_model_by = select_model_by
        self.features = None
        self.train_data_id = None
        self.target = None
        self.test_base_id = None
        self.models = None
        self.hyperparameters = None
        self.attributes = None
        self.recommendations = None
        self.options = None
        self.created_at = None
        self.updated_at = None
        self.completed_at = None

    @classmethod
    def create(cls, exp_id, name=None):
        """Create Experiment by exp_id.

        Args:
            exp_id(str): ObjectId in 24 hex digits
            name(str): (opt) Name to track Job progress

        Returns:
            class:`Experiment <Job>` object
        """
        core_service = CoreService()
        exp_resp = check_response(
            core_service.get_experiments_by_id(exp_id)).json()
        exp = cls(train_input=None)
        exp.update_result(exp_resp)
        exp.status = CoreXStatus.DONE
        exp.name = name
        return exp

    @update
    def update_result(self, task_result):
        """Update Job's attribute from Task's result."""
        self.get_best_model()

    def get_best_model(self):
        """Get the best model in experiment by `select_model_by`"""
        if not self.task.is_success():
            return
        class_ = self.__class__.__name__
        logger.debug('[%s] \'%s\' get best model', class_, self.name)
        model_list = self.attributes
        attr = self.select_model_by
        minlevel = {'mse', 'mae', 'mean_per_class_error'}
        best_model_id = None
        try:
            if self.select_model_by in minlevel:
                best_model_id = min(
                    model_list.values(),
                    key=lambda x: x['cv_averages'][attr])['model_id']
            else:
                best_model_id = max(
                    model_list.values(),
                    key=lambda x: x['cv_averages'][attr])['model_id']
        except AttributeError:
            logger.error('[%s] no models in %s result', class_, self.name)
        except KeyError as err:
            logger.error(err)

        if best_model_id is not None:
            self.best_model.update(self.id, best_model_id)
            self.best_model.task_status = self.task.status
            logger.debug(
                '[%s] \'%s\' best model id: %s',
                class_, self.name, best_model_id)
        else:
            logger.error(
                '[%s] fail to get best model', class_)


class ExperimentTS(Experiment, Job):
    """ExperimentTS manage to get the result from time series model training.

    Handle the execution of time series training task in order train
    time series model on coreX server. Stores the training results in
    ExperimentTS's attributes.

    Attributes:
        jobs(lst): [DataUpload]. List of jobs that ExperimentTS needs to wait
            till completed
        task(class:`TrainTSTask <CoreXTask>`):
            time series training task run by ExperimentTS Job
        train_input(class:`TrainTSInput <TrainTSInput>`):
            Settings for time series training models
        best_model(class:`MultiModel <MultiModel>`): MultiModel with the
            best score in `select_model_by` argument
        select_model_by(str): the score to select best model
        features(lst): The features used for training
        train_data_id(str): The ID of the train data
        target(str): The target of the experiment
        test_base_id(str): The ID for the test base data
        models(lst): The models' id of the experiment
        hyperparameters(JSON): The hyperparameters of the experiment
        attributes(JSON): The experiment attributes
        recommendations(JSON): Recommended model for each evaluator.
        created_at(str): The date the data was created
        options(JSON): Extra information for experiment
        updated_at(str): The time the data was last updated
        completed_at(str): The time the data was completed at
        name(str): Name to track Job progress
    """
    def __init__(self, train_input, select_model_by='mse', name=None):
        Job.__init__(
            self,
            jobs=[train_input.data],
            task=TrainTSTask(train_input, name=name),
            name=gen_id('ExpTS', name))

        self.train_input = train_input
        self.best_model = MultiModel()
        self.select_model_by = select_model_by
        self.features = None
        self.train_data_id = None
        self.target = None
        self.test_base_id = None
        self.models = None
        self.hyperparameters = None
        self.attributes = None
        self.recommendations = None
        self.options = None
        self.created_at = None
        self.updated_at = None
        self.completed_at = None

    @classmethod
    def create(cls, exp_id, name=None):
        """Create Time series Experiment by exp_id.

        Args:
            exp_id(str): ObjectId in 24 hex digits
            name(str): (opt) Name to track Job progress

        Returns:
            class:`ExperimentTS <Job>` object
        """
        return super(ExperimentTS, cls).create(exp_id=exp_id, name=name)
