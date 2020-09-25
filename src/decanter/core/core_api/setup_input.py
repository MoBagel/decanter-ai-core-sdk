import json

from decanter.core.core_api import CoreBody
from decanter.core.enums.algorithms import Algo
from decanter.core.enums.evaluators import Evaluator
from decanter.core.enums import check_is_enum


class SetupInput:
    def __init__(
        self, data, data_source, data_columns, callback=None, data_id=None,
        eda=None, preprocessing=None, version=None):

        self.data = data

        tmp_accessor = CoreBody.Accessor.create(uri='tmp_uri', format='csv')
        dataColumns = CoreBody.column_array(data_columns)
        self.setup_body = CoreBody.SetupBody.create(
            data_source=tmp_accessor,
            data_id='tmp_data_id',
            callback=callback,
            eda=eda,
            data_columns=dataColumns,
            preprocessing=preprocessing,
            version=version)

    def get_setup_params(self):
        """Using setup_body to create the JSON request body for setting data.

        Returns:
            :obj:`dict`
        """
        setattr(self.setup_body, 'data_id', self.data.id)
        setattr(self.setup_body, 'data_source', self.data.accessor)
        params = json.dumps(
            self.setup_body.jsonable(), cls=CoreBody.ComplexEncoder)
        params = json.loads(params)
        return params