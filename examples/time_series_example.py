"""
Run; python -m examples.time_series_example
"""
import os

from decanter import core
from decanter.core.core_api import TrainTSInput, PredictTSInput
# from decanter.core.jobs import DataUpload, Experiment


def main():
    """
    Example of running time series on decanter.
    """
    # Enable default logger for logging message
    core.enable_default_logger()

    # Create connection to decanter server, and set up basic settings.
    # Logger message:
    #   "[Context] connect healty :)" if success.
    context = core.Context.create(
        username='{usr}', password='{pwd}', host='{decantercoreserver}')

    # The Main object handles the calling of Decanter Core's API.
    client = core.CoreClient()

    train_file_path = '{file_path}'
    test_file_path = '{file_path}'
    train_file = open(train_file_path, 'r')
    test_file = open(test_file_path, 'r')

    # Upload data to Decanter server. Will Get the DataUpload result.
    train_data = client.upload(file=train_file)
    test_data = client.upload(file=test_file)

    # train_data = DataUpload.create(data_id = "{data_id}", name="train_data")
    # test_data = DataUpload.create(data_id = "{data_id}", name="test_data")

    # Settings for time series training.
    train_input = TrainTSInput(
        data=train_data, target='amount', forecast_horizon=7, gap=1,
        datetime_column='DATE', time_group='STOCKCODE', max_model=1,
        tolerance=0.9, evaluator='mse', max_window_for_feature_derivation=7,
        endogenous_features=['amount'], time_unit='day',
        regression_method='sum', classification_method='count')

    # Start train time series models.
    exp_ts = client.train_ts(
        train_input=train_input, select_model_by='mse', name='ExpTS')

    # Settings for predict time series model using PredictTSInput.
    predict_ts_input = PredictTSInput(data=test_data, experiment=exp_ts)

    # Start time series model prediction, get PredicTStResult in return.
    pred_ts_res = client.predict_ts(predict_input=predict_ts_input)

    # Use context.run() to block the above instructions, making sure all the
    # result will be done to further step.
    # Logger message:
    #     Job proccessing: Create a progress bar showing its current process.
    #     Job finished: "[Job] 'name' done status: 'final status' id: 'id'"
    context.run()

    # Print out the text result of prediction.
    print(pred_ts_res.show())

    if not os.path.exists('tmp'):
        os.makedirs('tmp')

    # Dwonload predict results in csv to local.
    pred_ts_res.download_csv(path='./tmp/pred_res.csv')

    context.close()


if __name__ == '__main__':
    main()
