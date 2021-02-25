# pylint: disable=E1101,R0904,W0611
"""Handle sending Decanter GP API requests.

  Basic Usage::

    gp_service = GPAPI()
    gp_service.get_data_list()
:meta private:
"""

import logging

import requests
from urllib3.exceptions import InsecureRequestWarning

import decanter.core as core

logger = logging.getLogger(__name__)
requests.packages.urllib3.disable_warnings()

class GPAPI:
    """Handle sending Decanter GP API requests."""
    def __init__(self):
        pass # are headers necessary?

    @staticmethod
    def requests_(http, url, json=None, data=None, files=None, headers=None):
        """Handle request sending to Decanter GP.

        Send corresponding Bearer Auth request by argument and handle
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
        bearer_auth = BearerAuth(core.Context.APIKEY) # TODO: custom authentication method -- will this work?
        url = core.Context.HOST + url

        try:
            if http == 'GET':
                return requests.get(url=url, auth=bearer_auth, verify=False)
            if http == 'POST':
                return requests.post(
                    url=url, json=json, data=data,
                    files=files, auth=bearer_auth, verify=False, headers=headers)
            if http == 'PUT':
                return requests.put(
                    url=url, json=json, data=data,
                    files=files, auth=bearer_auth, verify=False, headers=headers)
            if http == 'DELETE':
                return requests.delete(
                    url=url, json=json, data=data,
                    files=files, auth=bearer_auth, verify=False)

            raise Exception('[GP] No such HTTP Method.')

        except requests.exceptions.RequestException as err:
            logger.error('[GP] Request Failed :(')
            raise Exception(err)

    def get_project_by_id(self, project_id):
        """Get project information

        Endpoint: /v1/project/{project_id}

        Returns:
            class:`Response <Response>` object        
        """
        return self.requests_('GET', '/v1/project/%s' % project_id)
    
    def post_project_create(self, **kwargs):
        """Create new project on GP backend

        Endpoint: /v1/project/create

        Returns:
            class: `Response <Response>` object
        """
        return self.requests_('POST', '/v1/project/create', json=kwargs)

    def post_experiment_create(self, **kwargs):
        """Create new (train) experiment on GP backend
        
        Endpoint: /v1/experiment/create
        
        Returns:
            class: `Response <Response>` object
        """
        return self.requests_('POST', '/v1/experiment/create', json=kwargs)
    
    def post_prediction_predict(self, **kwargs):
        """Make prediction on GP backend
        
        Endpoint: /v1/prediction/predict
        
        Returns:
            class: `Response <Response>` object
        """
        return self.requests_('POST', '/v1/prediction/predict', json=kwargs)

    def post_table_upload(self, **kwargs):
        """ Upload dataset on GP backend

        Endpoint: /v1/table/upload

        Returns:
            class: `Response <Response>` object
        """
        return self.requests_('POST', '/v1/table/upload', json=kwargs)

    def put_table_update(self, **kwargs):
        """Setup dataset on GP backend
        
        Endpoint: /v1/table/update
        
        Returns:
            class: `Response <Response>` object
        """
        return self.requests_('PUT', '/v1/table/update', json=kwargs)

    def get_table_by_id(self, table_id):
        """Get table by id from GP backend, called by GPDataUpload's methods
        
        Endpoint: /v1/table/{table_id}
        
        Returns:
            class: `Response <Response>` object
        """
        return self.requests_('GET', '/v1/table/%s' % table_id)

    def get_table_csv_by_id(self, table_id):
        """Get table csv file by id from GP backend, called by GPDataUpload's methods
        
        Endpoint: /v1/table/{table_id}/csv
        
        Returns:
            class: `Response <Response>` object; downloads csv file
        """
        return self.requests_('GET', '/v1/table/%s/csv' % table_id)
    
    def get_experiments_by_id(self, experiment_id):
        """Get experiment metadata.

        Endpoint: /experiments/{experiment_id}

        Returns:
            class:`Response <Response>` object
        """
        return self.requests_('GET', '/v1/experiment/%s' % experiment_id)

    class BearerAuth(requests.auth.AuthBase):
        def __init__(self, apikey):
            self.apikey = apikey
        def __call__(self, r):
            r.headers["authorization"] = "Bearer " + self.apikey
            return r

        