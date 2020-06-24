# pylint: disable=C0103
# pylint: disable=too-many-arguments
# pylint: disable=too-few-public-methods
# pylint: disable-msg=too-many-locals
# pylint: disable=no-member
"""Settings for the Model Training and Time Series MultiModel Training."""
import json

from decanter.core.core_api import CoreBody


class TrainInput:
    """Train Input for Experiment Job.

    Settings for model training.

    Attributes:
        data (:class:`~decanter.core.jobs.data_upload.DataUpload`):
            Train data uploaded on Decanter Core server
        train_body (:class:`~decanter.core.extra.body_obj.TrainBody`):
            Request body for sending train api.

    Example:
        .. code-block:: python

            train_input = TrainInput(data=train_data, target='Survived',
            algos=["XGBoost"], max_model=2, tolerance=0.9)

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

    Settings for time series training.

    Attributes:
        data (:class:`~decanter.core.jobs.data_upload.DataUpload`): Train data uploaded on
            Decanter Core server
        train_body (:class:`~decanter.core.extra.body_obj.TrainTrainAutoTSBodyBody`):
            Request body for sending time series training api.
    """
    def __init__(
            self, data, target, datetime_column, endogenous_features,
            forecast_horizon, gap, time_unit, regression_method,
            classification_method, callback=None, max_iteration=None,
            max_window_for_feature_derivation=None, generation_size=None,
            mutation_rate=None, crossover_rate=None, tolerance=None,
            validation_percentage=None, max_model=None, seed=None,
            evaluator=None, max_run_time=None, apu=None, algos=None,
            nfold=None, balance_class=None, max_after_balance=None,
            sampling_factors=None, test_base_id=None, holdout_percentage=None,
            time_group=None, feature_types=None):

        self.data = data
        model_build_control = CoreBody.ModelBuildControl.create(
            tolerance=tolerance,
            validation_percentage=validation_percentage,
            max_model=max_model)

        genetic_algorithm = CoreBody.GeneticAlgorithmParams.create(
            max_iteration=max_iteration,
            max_window_for_feature_derivation=max_window_for_feature_derivation,
            generation_size=generation_size,
            mutation_rate=mutation_rate,
            crossover_rate=crossover_rate)

        build_control = CoreBody.BuildControl.create(
            model_build_control=model_build_control,
            seed=seed,
            evaluator=evaluator,
            max_run_time=max_run_time,
            apu=apu,
            genetic_algorithm=genetic_algorithm)

        model_spec = CoreBody.ModelSpec.create(
            endogenous_features=endogenous_features,
            algos=algos,
            nfold=nfold,
            balance_class=balance_class,
            max_after_balance=max_after_balance,
            sampling_factors=sampling_factors)

        feature_types = CoreBody.column_array(feature_types)

        group_by = CoreBody.TSGroupBy.create(
            time_unit=time_unit,
            regression_method=regression_method,
            classification_method=classification_method)

        input_spec = CoreBody.InputSpec.create(
            train_data_id='tmp_data_id',
            target=target,
            datetime_column=datetime_column,
            forecast_horizon=forecast_horizon,
            gap=gap,
            test_base_id=test_base_id,
            holdout_percentage=holdout_percentage,
            feature_types=feature_types,
            time_group=time_group,
            group_by=group_by)

        self.train_auto_ts_body = CoreBody.TrainAutoTSBody.create(
            callback=callback,
            build_control=build_control,
            model_spec=model_spec,
            input_spec=input_spec)

    def get_train_params(self):
        """Using train_auto_ts_body to create the JSON request body
        for time series training.

        Returns:
            :obj:`dict`
        """
        setattr(
            self.train_auto_ts_body.input_spec, 'train_data_id', self.data.id)
        params = json.dumps(
            self.train_auto_ts_body.jsonable(), cls=CoreBody.ComplexEncoder)
        params = json.loads(params)
        return params
