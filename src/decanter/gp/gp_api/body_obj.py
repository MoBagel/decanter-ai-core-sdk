"""GP Objects

The unit of the request body when sending corex apis. Support turning
each CoreX Object to json format.

"""
import json

from decanter.gp.extra.decorators import gp_obj


class ComplexEncoder(json.JSONEncoder):
    """Extending JSONEncoder

    Define own JSON Encoder for the object having the function `jsonable`. It will
    return Dictionary object is having `jsonable`.

    Returns:
        function: `jsonable`
    """

    def default(self, obj):
        if hasattr(obj, 'jsonable'):
            return obj.jsonable()
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


class GPBodyObj:
    """Base class of all GP Object.

    Has the jsonable function to return the Dictionary of object.

    """

    def __init__(self, **kwargs):
        """Add the argument pass in as attributes."""
        self.__dict__.update(
            (k, v) for k, v in kwargs.items() if v is not None)

    def jsonable(self):
        """Reutrn the Dictionary of Object"""
        return self.__dict__
