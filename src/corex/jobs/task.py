# pylint: disable=C0103
"""Task

Handle completing tasks such as upload data, train, prediction...ect.
Return the result to Job.
"""
import abc
import logging

from functools import partial

from corex import Context
from corex.core import CoreService
from corex.corex_vars import CoreXStatus, CoreXKeys
from corex.extra.utils import check_response, isnotebook, gen_id

logger = logging.getLogger(__name__)

try:
    if isnotebook():
        raise ImportError
except ImportError:
    from tqdm.notebook import tqdm
else:
    from tqdm import tqdm


class Task:
    """Handle Action's result

    Handle the execution of the actions (ex. upload data), the
    update of the results, and the tracking of status to determine
    the end of execution.

    Attributes:
        status(str): Status of task.
        result: The result of task, the type depends on the actions.
        name(str): (opt) Name of task for tracking process.
    """

    def __init__(self, name=None):
        self.status = CoreXStatus.PENDING
        self.result = None
        self.name = name

    def is_done(self):
        """Return True if Task is done, else False"""
        return self.status in CoreXStatus.DONE_STATUS

    def not_done(self):
        """Return True if Task is not done, else False"""
        return not self.is_done()

    def is_success(self):
        """Check if task has succeeded.

        Return True if both Task is done and have gotten result.

        Returns: Boolen
        """
        return self.status == CoreXStatus.DONE and self.result is not None

    def is_fail(self):
        """Check if Task failed.

        Return True if both Task is in fail status or done but without
        getting the result.

        Returns: Boolen
        """
        return self.status in CoreXStatus.FAIL_STATUS or \
            (self.status == CoreXStatus.DONE and self.result is None)

    @abc.abstractmethod
    def run(self):
        """Execute task

        Shoule Implement by child class.
        """
        raise NotImplementedError('Please Implement run method')

    @abc.abstractmethod
    async def update(self):
        """Update attribute by response or result.

        Shoule Implement by child class.
        """
        raise NotImplementedError('Please Implement update method')


class CoreXTask(Task):
    """Handle CoreX Action's result

    Handle the task relate to corex server, such as upload data,
    training, prediction.

    Global variable:
        BAR_CNT(int): The position of progress bar to avoid overlapping.

    Attributes:
        status(str): Status of task.
        result: The result of task, the type depends on the actions.
        name(str): (opt) Name of task for tracking process.
    """
    BAR_CNT = 0

    def __init__(self, name=None):
        super().__init__(name=name)
        self.core_service = CoreService()
        self.id = None
        self.response = None
        self.progress = 0
        self.pbar = None

    async def update(self):
        """Update the response from CoreX server.

        Get the task from sending api request and update the result
        of response.
        """
        func = partial(self.core_service.get_tasks_by_id, task_id=self.id)
        self.response = await Context.LOOP.run_in_executor(None, func)
        if self.status in CoreXStatus.DONE_STATUS:
            return
        self.response = check_response(self.response).json()
        self.update_task_response()
        logger.debug(
            '[Task]\'%s\' done update. status: %s', self.name, self.status)

    def update_task_response(self):
        """Update the result from response

        Update progress, and status. Update progress bar due to the
        value of responses['progress'].
        """
        logger.debug(
            '[Task] \'%s\' start update task resp. status: %s',
            self.name, self.status)

        def update_pbar(resp_progress):
            diff = int((resp_progress - self.progress)*100)
            self.pbar.update(diff)
            self.progress = resp_progress

        for key_ in [CoreXKeys.id, CoreXKeys.progress, CoreXKeys.result, CoreXKeys.status]:
            attr, key = key_.name, key_.value
            try:
                if key_ == CoreXKeys.progress:
                    update_pbar(self.response[key])
                setattr(self, attr, self.response[key])
            except KeyError as err:
                logger.debug(str(err))

    @abc.abstractmethod
    def run(self):
        """Execute CoreX task.

        Shoule Implement by child class.
        """
        raise NotImplementedError('Please Implement run method in CoreXTask')

    def run_corex_task(self, api_func, **kwargs):
        """Run CoreX Task
        Start CoreX task by calling api_func.
        Args:
            api_func(func): CoreService function
            kwargs: parameter for api_func
        """
        logger.debug('[%s] \'%s\' start.', self.__class__.__name__, self.name)
        self.response = check_response(
            api_func(**kwargs), key=CoreXKeys.id.value)
        self.response = self.response.json()
        self.id = self.response[CoreXKeys.id.value]
        logger.debug(
            '[%s] \'%s\' upload task id: %s',
            self.__class__.__name__, self.name, self.id)

        self.pbar = tqdm(
            total=100, position=CoreXTask.BAR_CNT, leave=True,
            bar_format='{l_bar}{bar}', desc='Progress %s' % self.name)
        CoreXTask.BAR_CNT += 1

        self.status = CoreXStatus.RUNNING

    def stop(self):
        """Stop undone task in CoreX server

        Send the stop task api to stop the running or pending task.
        """
        if self.id is not None:
            check_response(self.core_service.put_tasks_stop_by_id(self.id))
        logger.info(
            '[CoreXTask] Stop Task %s id:%s while %s',
            self.name, self.id, self.status)
        self.status = CoreXStatus.FAIL


class UploodTask(CoreXTask):
    """Upload data to CoreX.

    Attributes:
        file(csv-file-object): The csv file to be uploaded.
    """
    def __init__(self, file, name=None):
        super().__init__(name=gen_id('UploadTask', name))
        self.file = file

    def run(self):
        """
        Execute upload data by sending the upload api.
        """
        super().run_corex_task(
            api_func=self.core_service.post_upload,
            filename=self.file.name, file=self.file,
            encoding='text/plain(UTF-8)')


class TrainTask(CoreXTask):
    """Train model on CoreX.

    Attributes:
        train_input(class:`TrainInput <TrainInput>`): Settings for training.
    """
    def __init__(self, train_input, name=None):
        super().__init__(name=gen_id('TrainTask', name))
        self.train_input = train_input

    def run(self):
        train_params = self.train_input.get_train_params()
        super().run_corex_task(
            api_func=self.core_service.post_tasks_train,
            **train_params)


class TrainTSTask(CoreXTask):
    """Train time series model on CoreX.

    Attributes:
        train_input(class:`TrainTSInput <TrainTSInput>`):
            Settings for training.
    """
    def __init__(self, train_input, name=None):
        super().__init__(name=gen_id('TrainTSTask', name))
        self.train_input = train_input

    def run(self):
        train_params = self.train_input.get_train_params()
        super().run_corex_task(
            api_func=self.core_service.post_tasks_train_time_series,
            **train_params)


class PredictTask(CoreXTask):
    """Predict model on CoreX.

    Attributes:
        predict_input(class:`PredictInput <PredictInput>`):
            Settings for prediction.
    """
    def __init__(self, predict_input, name=None):
        super().__init__(name=gen_id('Pred_Task', name))
        self.predict_input = predict_input

    def run(self):
        pred_params = self.predict_input.getPredictParams()
        super().run_corex_task(
            api_func=self.core_service.post_tasks_predict,
            **pred_params)


class PredictTSTask(CoreXTask):
    """Predict time series model on CoreX.

    Attributes:
        predict_input(class:`PredictTSInput <PredictInput>`):
            Settings for time series prediction.
    """
    def __init__(self, predict_input, name=None):
        super().__init__(name=gen_id('PredTS_Task', name))
        self.predict_input = predict_input

    def run(self):
        pred_params = self.predict_input.getPredictParams()
        super().run_corex_task(
            api_func=self.core_service.post_tasks_predict_tsmodel,
            **pred_params)


class SetupTask(CoreXTask):
    """Predict time series model on CoreX.

    Attributes:
        predict_input(class:`PredictInput <PredictInput>`):
            Settings for prediction.
    """
    def __init__(self, params, name='Setup'):
        super().__init__(name=name)
        self.params = params

    def run(self):
        """
        Execute setup data by sending the setup api.
        """
        super().run_corex_task(
            api_func=self.core_service.post_tasks_setup,
            **self.params)
