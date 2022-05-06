from typing import List


def find_indices_of_substring(full_string: str, sub_string: str) -> List[int]:
    """Return a list of indices of substring matchings.

    Parameters
    ----------
    full_string : str
        The string to find occurrences of the substring in.
    sub_string : str
        The substring to find in the full string.

    Returns
    -------
    List[int]
        The list of indices.
    """
    return [
        index
        for index in range(len(full_string))
        if full_string.startswith(sub_string, index)
    ]


def str2int(input: str) -> int:
    """Parse a string to an integer. An empty string is interpreted as zero.

    Parameters
    ----------
    input : str
        The string.

    Returns
    -------
    int
        The integer.
    """
    if not input:
        return 0
    return int(input)