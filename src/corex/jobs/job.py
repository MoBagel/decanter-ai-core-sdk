# pylint: disable=invalid-name
"""Job

Handle the timeing of task's execution, and stores the result
of task in its attributes.
"""
import abc
import asyncio
import logging

from corex.core import CoreService
from corex.corex_vars import CoreXStatus
from corex.extra.decorators import block_method


logger = logging.getLogger(__name__)


class Job:
    """Handle he timeing of task's execution.

    Every Job will have to wait for all the other Jobs in jobs list to be
    success before it starts to run its task.

    Attributes:
        id(str): ObjectId in 24 hex digits
        status(str): Job status
        result(JSON): JOb result depends on type of Job
        task(class:`Task <Task>`): Task to be run by Job
        jobs(lst): List of class: `Job <Job>` that needs to be waited before
            running task
        name(str): Name to track Job progress
        core_service(class:`CoreService <CoreService>`): Handle the calling
            of api
    """
    def __init__(self, task, jobs=None, name=None):
        self.id = None
        self.status = CoreXStatus.PENDING
        self.result = None
        self.task = task
        self.jobs = jobs
        self.name = name
        self.core_service = CoreService()

    def is_done(self):
        """Return True if Job is done, else False"""
        return self.status in CoreXStatus.DONE_STATUS

    def not_done(self):
        """Return True if Job is not done"""
        return not self.is_done()

    def is_success(self):
        """Check if Job has succeeded.

        Return True if both Job is done and have gotten result.

        Returns: Boolen
        """
        return self.status == CoreXStatus.DONE and self.result is not None

    def is_fail(self):
        """Check if Job failed.

        Return True if both Job is in fail status or done but without
        getting the result.

        Returns: Boolen
        """
        return self.status in CoreXStatus.FAIL_STATUS or \
            (self.status == CoreXStatus.DONE and self.result is None)

    async def wait(self):
        """Mange the Execution of task.

        A python coroutine be wapped as task and put in event loop once a Job
        is created.  When the event loop starts to run, wait function will
        wait for prerequired jobs in self.jobs list to be done, and continue
        to execute running the task if all prerequired jobs is successful.

        The coroutine will be done when the Job fininsh gettng the result from
        task.
        """
        if self.jobs is not None and self.status not in CoreXStatus.DONE_STATUS:

            while not all(job.is_done() for job in self.jobs) and \
                    not any(job.is_fail() for job in self.jobs):
                ll = [job.status for job in self.jobs]
                logger.debug(
                    '[Job] \'%s\' waiting %s pre required jobs. jobs status: %s',
                    self.name, len(self.jobs), ll)
                await asyncio.sleep(5)

            # check if any pre_request_jobs has failed
            if not all(job.is_success() for job in self.jobs):
                message = ' '.join([job.status for job in self.jobs])
                self.status = CoreXStatus.FAIL
                logger.info(
                    '[Job] %s failed due to some job fail in jobs:[%s]',
                    self.name, message)

        if self.status in CoreXStatus.DONE_STATUS:
            logger.info('[Job] %s failed status: %s', self.name, self.status)
            return

        self.status = CoreXStatus.RUNNING
        self.task.run()

        while self.task.not_done():
            await self.update()
            if self.task.not_done():
                await asyncio.sleep(3)

        self.status = self.task.status
        logger.info(
            '[Job] \'%s\' done status: %s id: %s',
            self.name, self.status, self.id)
        return

    async def update(self):
        """Update attributes from task's result.

        A python coroutine await by `Job.wait()`.
        Will wait for task to update its result by await task.update(),
        then use the updated result from task to update Job's attributes.
        """
        await self.task.update()
        self.update_result(self.task.result)

    @abc.abstractmethod
    def update_result(self, task_result):
        """Implemented by child class"""
        raise NotImplementedError('Please Implement update_result method')

    def stop(self):
        """Stop Job

        Job will handle stoping itself by following conditions.
        job.status pending => mark as fail
        job.status running  => task pending => mark task fail => mark job fail
                            => task.status running
                                => call stop api & update task status
                                => mark job.status fail
                            => task status in done => mark job status fail
        job in done status => do nothing log(already done)
        """
        if self.status == CoreXStatus.PENDING:
            self.status = CoreXStatus.FAIL
        elif self.status == CoreXStatus.RUNNING:
            if self.task.status not in CoreXStatus.DONE_STATUS:
                self.task.stop()
            self.status = CoreXStatus.FAIL
        else:
            logger.info(
                '[Job] %s have finished already status %s',
                self.name, self.status)

        logger.info('[Job] %s stop successfully', self.name)

    @block_method
    def get(self, attr):
        """get Job's attribute

        If it calls this function while Job is still undone, will appears
        message for remind.
        """
        return getattr(self, attr)
