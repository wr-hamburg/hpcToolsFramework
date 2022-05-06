from typing import List


def values_of_object(obj) -> List:
    """Return a list of all attribute values of an object.
    This excludes callables.

    Parameters
    ----------
    obj : _type_
        The specified object.

    Returns
    -------
    List
        A list of the attribute values.
    """
    return [
        getattr(obj, attr)
        for attr in dir(obj)
        if not attr.startswith("__") and not callable(getattr(obj, attr))
    ]