[![PyPI version](https://badge.fury.io/py/decanter-ai-core-sdk.svg)](https://pypi.org/project/decanter-ai-core-sdk/)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/MoBagel/decanter-ai-core-sdk)

# MoBagel Decanter AI Core SDK

Decanter AI Core SDK allows you to call Decanter's API with more easy-to-use
functions in Python.

It makes actions such like upload data, train models, predict results run more
efficiently and handles hard to get results more accessible. It also supports
running in jupyter notebook.

## Installing
Install and update using pip:
```bash
pip install decanter-ai-core-sdk
```

## Simple Example
```python
from decanter import core

core.enable_default_logger()
context = core.Context.create(
        username='{usr}', password='{pwd}', host='{decanter-core-server}')
client = core.CoreClient()

train_file = open(train_file_path , 'r')
train_data = client.upload(file=train_file, name="train")

# In jupyter notebook just run the block no need to call context.run()
context.run()

train_data.show()
```

```bash
$ python -m path_to_file.file
15:50:09 [    INFO] [Context] no event loop to close
15:50:09 [    INFO] [Context] connect healty :)
Progress UploadTask_train:  55%|█████████████████████████████████████████
```

## Contributing
For guidance on setting up a development environment and how to make a
contribution to Decanter AI Core SDK, see the contributing guidelines.


## Links
For details on design, guidance on setting up a development environment and
how to make a contribution to MoBagel Decanter Core SDK.

* Code: https://github.com/MoBagel/decanter-ai-core-sdk
