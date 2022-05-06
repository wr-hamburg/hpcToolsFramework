from typing import List, TypeVar

T = TypeVar("T")


def single_or_default(collection: List[T], attr: str, value: str, default=None) -> T:
    """Return the first single element from the list which specified attribute matches the value.

    Parameters
    ----------
    collection : List[T]
        The list.
    attr : str
        The attribute of the list elements that we use to find the element.
    value : str
        The value of the attribute that we want to use to find the element.
    default : Any, optional
        A default value which is retured if no matching element is found, by default None.

    Returns
    -------
    T
        Returns the first matching element from the list.
    """
    l_collection = [elem for elem in collection if getattr(elem, attr) == value]
    if l_collection:
        return l_collection[0]
    else:
        return default


def is_list_of_strings(lst: List) -> bool:
    """Checks whether each element in the list is of type string.

    Parameters
    ----------
    lst : List
        The list.

    Returns
    -------
    bool
        Returns True if each list element is a string, otherwise False.
    """
    if lst and isinstance(lst, list):
        return all(isinstance(elem, str) for elem in lst)
    else:
        return False