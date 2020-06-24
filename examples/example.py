# pylint: disable=unsubscriptable-object
"""
Run: python -m docs.example
"""
import os

import pandas as pd

import corex
from corex import TrainInput, PredictInput
# from corex.jobs import DataUpload, Experiment


def main():
    """
    Example of training titanic dataset.
    """

    # Enable default logger for logging message
    corex.enable_default_logger()

    # Create connection to corex server, and set up basic settings.
    # Logger message:
    #   "[Context] connect healty :)" if success.
    context = corex.Context.create(
        username='{usr}', password='{pwd}', host='{corexserver}')

    # The Main object handles the calling of CoreX's API.
    client = corex.CoreXAPI()

    dir_path = os.getcwd()
    train_file_path = dir_path + '/docs/data/train.csv'
    test_file_path = dir_path + '/docs/data/test.csv'
    train_file = open(train_file_path, 'r')
    test_df = pd.read_csv(test_file_path)

    # Upload data to CoreX server. Will Get the DataUpload result.
    train_data = client.upload(file=train_file, name='train')
    test_data = client.upload(file=test_df, name='test')

    # Create DataUpload by exist data id
    # train_data = DataUpload.create(data_id="{data_id}", name="titanic_train")
    # test_data = DataUpload.create(data_id="{data_id}", name="titanic_test")

    # Use context.run() to block the above instructions, making sure all the
    # result will be done to further step.
    # Logger message:
    #     Job proccessing: Create a progress bar showing its current process.
    #     Job finished: "[Job] 'name' done status: 'final status' id: 'id'"
    context.run()

    # Set up data to change data type.
    train_data = client.setup(
        data_source={
            'uri': test_data.accessor['uri'],
            'format': 'csv'
            },
        data_id=test_data.id,
        data_columns=[
            {
                'id': 'Survived',
                'data_type': 'categorical'
            }, {
                'id': 'Age',
                'data_type': 'numerical'
            }],
        name='mysetup')

    # Settings for training model using TrainInput.
    train_input = TrainInput(
        data=train_data, target='Survived',
        algos=['XGBoost'], max_model=2, tolerance=0.9)

    # Start Model Training, get Experiment result in return.
    exp = client.train(
        train_input=train_input, select_model_by='mean_per_class_error',
        name='myexp')

    # Settings for predict model using PredictInput.
    predict_input = PredictInput(data=test_data, experiment=exp)

    # Start model prediction, get PredictResult in return.
    pred_res = client.predict(predict_input=predict_input, name='mypred')

    # Run all the actions above and make sure all is done before continue
    # to next step.
    context.run()

    # Print out the text result of prediction.
    print(pred_res.show())

    if not os.path.exists('tmp'):
        os.makedirs('tmp')

    # Download model zipped file to local.
    exp.best_model.download(model_path='./tmp/mymodel.zip')

    # Dwonload predict results in csv to local.
    pred_res.download_csv(path='./tmp/pred_res.csv')

    # Close context, close event loop and reset connections.
    context.close()


if __name__ == '__main__':
    main()
