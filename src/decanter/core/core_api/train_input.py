# pylint: disable=C0103
# pylint: disable=too-many-arguments
# pylint: disable=too-few-public-methods
# pylint: disable-msg=too-many-locals
# pylint: disable=no-member
"""Settings for the Model Training and Time Series MultiModel Training."""
import json

from decanter.core.core_api import CoreBody
from decanter.core.enums.algorithms import Algo
from decanter.core.enums.evaluators import Evaluator
from decanter.core.enums import check_is_enum

class TrainInput:
    """Train Input for Experiment Job.

    Settings for model training.

    Attributes:
        data (:class:`~decanter.core.jobs.data_upload.DataUpload`):
            Train data uploaded on Decanter Core server
        train_body (:class:`~decanter.core.core_api.body_obj.TrainBody`):
            Request body for sending train api.

    Example:
        .. code-block:: python

            train_input = TrainInput(data=train_data, target='Survived',
            algos=Algo.XGBoost, max_model=2, tolerance=0.9)

    """
    def __init__(
            self, data, target, algos,
            callback=None, test_base_id=None, test_data_id=None,
            evaluator=None, features=None, feature_types=None,
            max_run_time=None, max_model=None, tolerance=None, nfold=None,
            ts_split_split_by=None, ts_split_cv=None, ts_split_train=None,
            ts_split_test=None, seed=None, balance_class=None,
            max_after_balance=None, sampling_factors=None,
            validation_percentage=None, holdout_percentage=None, apu=None,
            preprocessing=None, version=None):

        evaluator = check_is_enum(Evaluator, evaluator)
        algos =  [check_is_enum(Algo, algo) for algo in algos]
        self.data = data
        if ts_split_train is None:
            train = None
        else:
            train = CoreBody.CVTrain.create(
                start=ts_split_train['start'], end=ts_split_train['end'])

        if ts_split_test is None:
            test = None
        else:
            test = CoreBody.CVTrain.create(
                start=ts_split_test['start'], end=ts_split_test['end'])

        cv = CoreBody.cv_obj_array(ts_split_cv)

        time_series_split = CoreBody.TimeSeriesSplit.create(
            split_by=ts_split_split_by,
            cv=cv,
            train=train,
            test=test)

        self.train_body = CoreBody.TrainBody.create(
            target=target,
            train_data_id='tmp_data_id',
            algos=algos,
            callback=callback,
            test_base_id=test_base_id,
            test_data_id=test_data_id,
            evaluator=evaluator,
            features=features,
            feature_types=feature_types,
            max_run_time=max_run_time,
            max_model=max_model,
            tolerance=tolerance,
            nfold=nfold,
            time_series_split=time_series_split,
            seed=seed,
            balance_class=balance_class,
            max_after_balance=max_after_balance,
            sampling_factors=sampling_factors,
            validation_percentage=validation_percentage,
            holdout_percentage=holdout_percentage,
            apu=apu,
            preprocessing=preprocessing,
            version=version)

    def get_train_params(self):
        """Using train_body to create the JSON request body for training.

        Returns:
            :obj:`dict`
        """
        setattr(self.train_body, 'train_data_id', self.data.id)
        params = json.dumps(
            self.train_body.jsonable(), cls=CoreBody.ComplexEncoder)
        params = json.loads(params)
        return params


class TrainTSInput:
    """Train Input for ExperimentTS Job.

    Settings for auto time series forecast training.

    Attributes:
        data (:class:`~decanter.core.jobs.data_upload.DataUpload`): Train data uploaded on
            Decanter Core server
        train_body (:class:`~decanter.core.core_api.body_obj.TrainAutoTSBody`):
            Request body for sending time series training api.
    """
    def __init__(
            self, data, target, datetime_column, forecast_horizon, gap, feature_types=None,
            callback=None, version='v2', max_iteration=None, generation_size=None,
            mutation_rate=None, crossover_rate=None, tolerance=None, validation_percentage=None,
            holdout_percentage=None, max_model=None, seed=None, evaluator=None,
            max_run_time=None, nfold=None, time_unit=None, numerical_groupby_method=None,
            categorical_groupby_method=None, endogenous_features=None, exogenous_features=None,
            time_groups=None, max_window_for_feature_derivation=None):

        evaluator = check_is_enum(Evaluator, evaluator)
        self.data = data

        geneticAlgorithm = CoreBody.GeneticAlgorithmParams.create(
            max_iteration=max_iteration,
            generation_size=generation_size,
            mutation_rate=mutation_rate,
            crossover_rate=crossover_rate
        )
        build_spec = CoreBody.BuildSpec.create(
            tolerance=tolerance,
            validation_percentage=validation_percentage,
            holdout_percentage=holdout_percentage,
            max_model=max_model,
            seed=seed,
            evaluator=evaluator,
            max_run_time=max_run_time,
            genetic_algorithm=geneticAlgorithm,
            nfold=nfold
        )
        group_by = CoreBody.TSGroupBy.create(
            time_unit=time_unit,
            numerical_groupby_method=numerical_groupby_method,
            categorical_groupby_method=categorical_groupby_method
        )
        input_spec = CoreBody.InputSpec.create(
            train_data_id='tmp_data_id',
            target=target,
            endogenous_features=endogenous_features,
            exogenous_features=exogenous_features,
            datetime_column=datetime_column,
            forecast_horizon=forecast_horizon,
            gap=gap,
            feature_types=feature_types,
            time_groups=time_groups,
            max_window_for_feature_derivation=max_window_for_feature_derivation,
            group_by=group_by
        )

        self.train_auto_ts_body = CoreBody.TrainAutoTSBody.create(
            callback=callback,
            version=version,
            build_spec=build_spec,
            input_spec=input_spec
        )

    def get_train_params(self):
        """Using train_auto_ts_body to create the JSON request body
        for time series forecast training.

        Returns:
            :obj:`dict`
        """
        setattr(self.train_auto_ts_body.input_spec, 'train_data_id', self.data.id)
        params = json.dumps(self.train_auto_ts_body.jsonable(), cls=CoreBody.ComplexEncoder)
        params = json.loads(params)
        return params
