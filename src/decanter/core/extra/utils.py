"""
Functions support other modules.
"""
import uuid


def check_response(response, key=None):
    """CHeck the api response.

    Make sure the status call is successful and the response have specific key.

    Return:
        class: `Response <Response>`
    """
    code = response.status_code
    if not 200 <= code < 300:
        raise Exception('[Decanter Core response Error] Request Error')

    if key is not None and key not in response.json():
        raise KeyError('[Decanter Core response Error] No key value')

    return response


def gen_id(type_, name):
    """Generate a random UUID if name isn't given.
    Returns:
        string
    """
    if name is None:
        rand_id = uuid.uuid4()
        rand_id = str(rand_id)[:8]
        name = type_ + '_' + rand_id

    return name


def isnotebook():
    """Return True if SDK is running on Jupyter Notebook."""
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole

        if shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython

        return False
    except NameError:
        return False
