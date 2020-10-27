# pylint: disable=E1101,R0904,W0611
"""Handle sending Decanter Core API requests.

  Basic Usage::

    core_service = CoreAPI()
    core_service.get_data_list()
:meta private:
"""
import logging

import requests
from requests.auth import HTTPBasicAuth
from urllib3.exceptions import InsecureRequestWarning

import decanter.core as core

logger = logging.getLogger(__name__)
requests.packages.urllib3.disable_warnings()


class CoreAPI:
    """Handle sending Decanter Core API requests."""
    def __init__(self):
        self._corex_headers = {'user': 'sdk'}

    @property
    def corex_headers(self):
        return self._corex_headers

    @staticmethod
    def requests_(http, url, json=None, data=None, files=None, headers=None):
        """Handle request sending to Decanter Core.

        Send corresponding Basic Auth request by argument and handle
        RequestException.

        Args:
            http: string, http method.
            url: string, url endpoint.
            json: (opt) JSON Python object to send in the request body.
            data: (opt) dictionary, list of tuples, bytes, or file-like
                object to send in the body of request.
            files: (opt) dictionary, {'name': file-like-objects}
                (or {'name': file-tuple}) for multipart encoding upload.
            headers: (opt) dictionary, particular headers that decanter ai support,
                {'user': 'sdk'} for decanter to know task source is from
                decanter-ai-core-sdk.

        Returns:
            class:`Response <Response>` object

        Raises:
            Exception: Occurred when raises RequestException
                    or calling wrong http method.
        """
        basic_auth = HTTPBasicAuth(core.Context.USERNAME, core.Context.PASSWORD)
        url = core.Context.HOST + url
        try:
            if http == 'GET':
                return requests.get(url=url, auth=basic_auth, verify=False)
            if http == 'POST':
                return requests.post(
                    url=url, json=json, data=data,
                    files=files, auth=basic_auth, verify=False, headers=headers)
            if http == 'PUT':
                return requests.put(
                    url=url, json=json, data=data,
                    files=files, auth=basic_auth, verify=False, headers=headers)
            if http == 'DELETE':
                return requests.delete(
                    url=url, json=json, data=data,
                    files=files, auth=basic_auth, verify=False)

            raise Exception('[Core] No such HTTP Method.')

        except requests.exceptions.RequestException as err:
            logger.error('[Core] Request Failed :(')
            raise Exception(err)

    def get_data_list(self):
        """Get list of data metadata.

        Endpoint: /data

        Returns:
            class:`Response <Response>` object
        """
        return self.requests_(http='GET', url='/data')

    def get_data_by_id(self, data_id):
        """Get data metadata.

        Endpoint: /data/{data_id}

        Returns:
            class:`Response <Response>` object
        """
        return self.requests_(http='GET', url='/data/%s' % data_id)

    def delete_data_by_id(self, data_id):
        """Delete data metadata.

        Endpoint: /data/{data_id}

        Returns:
            class:`Response <Response>` object
        """
        return self.requests_(http='DELETE', url='/data/delete%s' % data_id)

    def get_data_file_by_id(self, data_id):
        """Download csv file of data.

        Endpoint: /data/{data_id}/file

        Returns:
            class:`Response <Response>` object
        """
        return self.requests_(http='GET', url='/data/%s/file' % data_id)

    def post_data_delete(self, **kwargs):
        """Batch delete data.

        Endpoint: /data/{data_id}

        Returns:
            class:`Response <Response>` object
        """
        return self.requests_(http='POST', url='/data/delete', json=kwargs)

    def post_upload(self, **kwargs):
        """Upload csv file and setup data.

        Endpoint: /v2/upload

        Returns:
            class:`Response <Response>` object
        """
        files = {
            'csv': (
                kwargs['filename'],
                kwargs['file'],
                kwargs['encoding']
            )
        }
        return self.requests_(http='POST', url='/v2/upload', files=files, headers=self.corex_headers)

    def get_tasks_by_id(self, task_id):
        """Get the task by task_id.

        Endpoint: /tasks/{task_id}

        Returns:
            class:`Response <Response>` object
        """
        return self.requests_(http='GET', url='/tasks/%s' % task_id)

    def get_tasks_list(self):
        """Get list of tasks.

        Endpoint: /tasks

        Returns:
            class:`Response <Response>` object
        """
        return self.requests_(http='GET', url='/tasks')

    def put_tasks_stop_by_id(self, task_id):
        """Stop a running or pending task.

        Endpoint: /tasks/{task_id}/stop

        Returns:
            class:`Response <Response>` object
        """
        return self.requests_(http='PUT', url='/tasks/%s/stop' % task_id, headers=self.corex_headers)

    def post_tasks_setup(self, **kwargs):
        """Setup data reference.

        Endpoint: /v2/tasks/setup

        Returns:
            class:`Response <Response>` object
        """
        return self.requests_(http='POST', url='/v2/tasks/setup', json=kwargs, headers=self.corex_headers)

    def post_tasks_train(self, **kwargs):
        """Train model from data reference.

        Endpoint: /v2/task/train

        Returns:
            class:`Response <Response>` object
        """
        return self.requests_(http='POST', url='/v2/tasks/train', json=kwargs, headers=self.corex_headers)

    def post_tasks_auto_ts_train(self, **kwargs):
        """Train time series forecast multi model from data reference.

        Endpoint: /v2/tasks/auto_ts/train

        Returns:
            class:`Response <Response>` object
        """
        return self.requests_(
            http='POST', url='/v2/tasks/auto_ts/train', json=kwargs, headers=self.corex_headers)


    def post_tasks_predict(self, **kwargs):
        """Predict from model.

        Endpoint: /v2/tasks/predict

        Returns:
            class:`Response <Response>` object
        """
        return self.requests_(
            http='POST', url='/v2/tasks/predict', json=kwargs, headers=self.corex_headers)

    def post_tasks_auto_ts_predict(self, **kwargs):
        """Predict from time series forecast model.

        Endpoint: /v2/tasks/auto_ts/predict

        Returns:
            class:`Response <Response>` object
        """
        return self.requests_(
            http='POST', url='/v2/tasks/auto_ts/predict', json=kwargs, headers=self.corex_headers)

    def get_experiments_by_id(self, exp_id):
        """Get experiment metadata.

        Endpoint: /experiments/{experiment_id}

        Returns:
            class:`Response <Response>` object
        """
        return self.requests_(http='GET', url='/experiments/%s' % exp_id)

    def get_models_by_id(self, exp_id, model_id):
        """Get model metadata.

        Endpoint: /v2/experiments/{exp_id}/models/{model_id}

        Returns:
            class:`Response <Response>` object
        """
        return self.requests_(
            http='GET', url='/v2/experiments/%s/models/%s' % (exp_id, model_id))

    def get_models_download_by_id(self, model_id):
        """Get model mojo file.

        Endpoint: /data/{data_id}

        Returns:
            class:`Response <Response>` object
        """
        return self.requests_(http='GET', url='/models/%s/download' % model_id)

    def get_multimodels_by_id(self, exp_id, model_id):
        """Get multimodel meta data by model_id which trained in the experiment.

        Endpoint: /auto_ts/experiments/{exp_id}/models/{model_id}

        Returns:
            class:`Response <Response>` object
        """
        return self.requests_(
            http='GET',
            url='/auto_ts/experiments/%s/models/%s' % (exp_id, model_id))

    def get_worker_count(self):
        """Get counts of each type of worker

        Endpoint: /worker/count

        Returns:
            class: `Response <Response>` object
        """
        return self.requests_(
            http='GET',
            url='/worker/count')

    def get_worker_status(self):
        """List status of each worker

        Endpoint: /worker/status

        Returns:
            class: `Response <Response>` object
        """
        return self.requests_(
            http='GET',
            url='/worker/status')
