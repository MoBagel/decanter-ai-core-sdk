"""Initialization for running SDK.

  Typical usage example:

  context = Context.create(username='usr', password='pwd', host='corex-server')
  context.run()
"""
import asyncio
import logging

import pandas as pd
import requests
from requests.auth import HTTPBasicAuth


logger = logging.getLogger(__name__)


class Context:
    """Init the connection to corex server and functionality for running SDK.

    Attributes:
        USERNAME: A string for user name to login in corex server.
        PASSWORD: A string for password to login in corex server.
        HOST: A string of corex server's URL.
        LOOP: Event Loop of Asynchronous I/O.
        CORO_TASKS: List of tasks that wrapped from coroutines.
        JOBS: List of finished and waited Jobs.
    """
    USERNAME = None
    PASSWORD = None
    HOST = None
    LOOP = None
    CORO_TASKS = []
    JOBS = []

    def __init__(self):
        pass

    @classmethod
    def create(cls, username, password, host):
        """Create conext instance and init neccessary variable and objects.

        Setting the user, password, and host for the funture connection when
        calling APIs, and create an event loop if it isn't exist. Check if the
        connection is healthy after args be set.

        Args:
            username: User name for login corex server.
            password: Password name for login corex server.
            host: CoreX server URL.

        Returns:
            A context instance.
        """
        context = cls()
        context.close()
        Context.USERNAME = username
        Context.PASSWORD = password
        Context.HOST = host

        # get the current event loop
        # it will create a new event loop if it does not exist
        Context.LOOP = asyncio.get_event_loop()

        # if the current loop is closed create a new one
        if Context.LOOP.is_closed():
            asyncio.set_event_loop(asyncio.new_event_loop())
            Context.LOOP = asyncio.get_event_loop()
            logger.debug('[Context] create and set new event loop')

        context.healthy()
        return context

    @staticmethod
    def run():
        """Start execute the tasks in CORO_TASKs.

        Gather all tasks and execute.  It will block on all tasks until all
        have been finished.
        """
        logger.debug('Run %s coroutines', len(Context.CORO_TASKS))

        if Context.LOOP is None:
            logger.error('[Context] create context before run')
            raise Exception()

        if Context.LOOP.is_running() is False:
            groups = asyncio.gather(*Context.CORO_TASKS)
            Context.LOOP.run_until_complete(groups)
            Context.CORO_TASKS = []

    @staticmethod
    def close():
        """Close the event loop and reset JOBS and CORO_TASKS.

        Close the event loop if it's not running (will not close in
        Jupyter Notebook).
        """
        logger.debug('[Context] try to close context')
        if Context.LOOP is not None:
            Context.LOOP = asyncio.get_event_loop()
            if Context.LOOP.is_running() is False:
                Context.LOOP.close()
                logger.info('[Context] close event loop successfully')
        else:
            logger.info('[Context] no event loop to close')
        logger.debug('[Context] remain CORO TASKS %s', len(Context.CORO_TASKS))
        Context.JOBS = []
        Context.CORO_TASKS = []
        Context.USERNAME = Context.PASSWORD = Context.HOST = None

    @staticmethod
    def healthy():
        """Check the connection between corex.

        Send a fake request to determine if there's connection or
        authorization errors.
        """
        try:
            url = '%s/data/test' % Context.HOST
            res = requests.delete(
                url, auth=HTTPBasicAuth(Context.USERNAME, Context.PASSWORD),
                timeout=2)
            if res.status_code != 400:
                raise Exception()
        except (Exception, requests.exceptions.RequestException) as err:
            logger.error('[Context] connect not healthy :(')
            raise SystemExit(err)
        else:
            logger.info('[Context] connect healty :)')

    @staticmethod
    def get_all_jobs():
        """Get a list of Jobs that have been or waiting to be executed.

        Returns:
            A list of Jobs.
        """
        return Context.JOBS

    @staticmethod
    def get_jobs_status():
        """Get a dataframe of all jobs and its corresponding status.

        Returns:
            A pandas dataframe.
        """
        jobs_status = {
            'Job': [],
            'status': []
        }
        for job in Context.JOBS:
            jobs_status['Job'].append(job.name)
            jobs_status['status'].append(job.status)

        return pd.DataFrame(jobs_status)

    @staticmethod
    def stop_jobs(jobs_list):
        """Stop Jobs in jobs_list.

        Args:
            jobs_list: list of jobs instance wish to be stopped.
        """
        for job in jobs_list:
            job.stop()

    @staticmethod
    def stop_all_jobs():
        """Stop all Jobs"""
        for job in Context.JOBS:
            if job.status not in ['done', 'fail', 'invalid']:
                job.stop()
