[![PyPI version](https://badge.fury.io/py/decanter-ai-core-sdk.svg)](https://pypi.org/project/decanter-ai-core-sdk/)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/MoBagel/decanter-ai-core-sdk)

# MoBagel Decanter AI Core SDK

Decanter AI is a powerful AutoML tool which enables everyone to build ML models and make predictions without data science background. With Decanter AI Core SDK, you can integrate Decanter AI into your application more easily with Python. 

It supports actions such as data uploading, model training, and prediction to run in a more efficient way and access results more easily. You can also use Decanter AI Core SDK in Jupyter Notebook for better visualization.

To know more about Decanter AI and how you can be benefited with AutoML, visit [MoBagel website](https://mobagel.com/product/) and contact us to try it out!

## System Requirement
* python3.7


## Install
Install and update using pip:
```bash
pip install decanter-ai-core-sdk
```


## Basic Example: Upload Data
```python
from decanter import core

core.enable_default_logger()
client = core.CoreClient(
        username='gp', password='gp-admin', host='http://host:port')

train_file = open(train_file_path, 'r')
train_data = client.upload(file=train_file, name="train")

# in jupyter notebook just run the block
# no need to call context.run()
client.run()

train_data.show()
```

```bash
$ python -m example.file
15:50:09 [    INFO] [Context] no event loop to close
15:50:09 [    INFO] [Context] connect healthy :)
Progress UploadTask_train:  55%|█████████████████████████████████████████
```

## Example Dataset Path 
* `examples/data/` - store the general dataset
* `examples/data/ts_data` - store the time series dataset


## Example Code
* General Data
	* Python Script: [example.py](https://github.com/MoBagel/decanter-ai-core-sdk/blob/master/examples/example.py)
	* Jupyter: [jupyter_example.ipynb](https://github.com/MoBagel/decanter-ai-core-sdk/blob/master/examples/jupyter_example.ipynb)
* Time Series Data
	* Python Script: [auto_time_series_example.py](https://github.com/MoBagel/decanter-ai-core-sdk/blob/master/examples/auto_time_series_example.py)  

Note:  
Since Jupyter already have an event loop (asyncio), SDK will just use the current event loop. See more in [here](https://www.notion.so/API-615d2fba4e7f45c4b5fe63cc192e481f#bb4f0a4b2847450abc4f80b025469170).  
More details about asyncio in [learn asyncio](https://docs.python.org/3/library/asyncio.html)
```python
import asyncio
loop = asyncio.get_running_loop()
loop.is_running()
```

## Tutorial for Jupyter Notebook
If you want to learn how to build ML models with Decanter AI, visit our [jupyter_example.ipynb](https://github.com/MoBagel/decanter-ai-core-sdk/blob/master/examples/jupyter_example.ipynb) for step by step tutorial.
If you need to handle running tasks well, refer to our [jupyter_jobs_handle_example.ipynb](https://github.com/MoBagel/decanter-ai-core-sdk/blob/master/examples/jupyter_jobs_handle_example.ipynb).


## Development Guide and Flow
* If you are curious about why Decanter AI Core SDK does certain things the way it does and not differently, visit our [Development Guide](https://mobagel.github.io/decanter-ai-core-sdk/notes/design.html)


## Documentation
To understand how we design Decanter AI Core SDK, `doc/` contains the complete documentation, including the design system, the use of each API, and the required dependencies to install. Refer to our [document page](https://mobagel.github.io/decanter-ai-core-sdk/index.html) to navigate the complete information.


## Contributing
For guidance on setting up a development environment and how to make a contribution to Decanter AI Core SDK, see the [contributing guidelines](https://mobagel.github.io/decanter-ai-core-sdk/notes/contributing.html).


## Links
For more details on design, guidance on setting up a development environment, and SDK usage.

* Decanter AI Introduction: https://mobagel.com/product/
* Decanter AI SDK Introduction: https://mobagel.github.io/decanter-ai-core-sdk/
* Code: https://github.com/MoBagel/decanter-ai-core-sdk
* Installation: https://mobagel.github.io/decanter-ai-core-sdk/user/install.html
* API interface: https://mobagel.github.io/decanter-ai-core-sdk/api.html