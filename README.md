# Mobagel CoreX Python SDK
Mobagel CoreX allows you to call CoreX APIs with more easy-to-use functions in Python.
It makes actions such like upload data, train models, predict results run more efficiently and handles hard to get results more accessible. It also supports running in jupyter notebook.

## Installing
### Virtual Environments
Use a virtual environment to manage the dependencies for your project, both in development and in production.
* Install [Anaconda](https://www.anaconda.com/distribution/#macos) or [Virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).
* Create and activate vitrual environment.
    * Conda
    ```
    conda create -n myenv python=3.6
    conda activate myenv
    ```
    * Vitualenv
    ```bash
    virtualenv myenv
    source myenv/bin/activate
    ```

### Install Mobagel CoreX
Install and update using pip:
```python
pip install mobagel-corex --extra-index-url=https://test.pypi.org/simple/
```

## Quick Start
Activate your virtual environments.

Clone the repository from GitLab:
```bash
git clone git@gitlab.ct.mobagel.com:GEN/corex-python-sdk.git
```
Since it's not published, checkout to latest branch
```bash
cd corex-python-sdk
git checkout python_future
```
### Run in Python Script

Set the username, password, and host at function `context.create()` in file `docs/example.py` 
```python
context = Context.create(username='your-username', password='your-password', host='mobagel-corex-server')
```
Run the command below:
```bash
python -m docs.example
```
### Run in Jupyter Notebook
Install Jupyter Notebook.
```bash
pip install jupyter notebook
```
Add virtual environment to Jupyter Notebook. Make sure ipykernel is installed in the virtual environment.
```bash
pip install --user ipykernel
python -m ipykernel install --user --name=myenv
# following output
# Installed kernelspec myenv in /home/user/.local/share/jupyter/kernels/myenv
```
Open jupyter notebook
```bash
jupyter notebook
```
Open the notebook in `docs/example.ipynb`, and select the kernel of your environment in the above tool bar `Kernal/Change kernel/myenv`

## Links
For details on design, guidance on setting up a development environment and how to make a contribution to Mobagel-CoreX.
* Documentation: https://www.notion.so/SDK-34c9a6d0ac61493aafd6a0433cfa7c5a
* Development: https://www.notion.so/Development-56ed1e780d304f8386af7d1dfffef2b0
* Releases: https://test.pypi.org/project/mobagel-corex/