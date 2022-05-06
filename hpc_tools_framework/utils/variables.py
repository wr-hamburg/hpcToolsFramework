import logging
from typing import Dict, List
from hpc_tools_framework.utils import find_indices_of_substring
from hpc_tools_framework.constants import (
    OUTPUT_VAR,
    INPUT_VAR,
    HOME_VAR,
    CPU_VAR,
    SET_VAR,
)


class Variables:
    """A container class to manage all variables."""

    def __init__(self):
        self._vars = dict()
        """A dictionary to store all variables and their values."""

    def set_output(self, value: str) -> None:
        """Set the output variabel.

        Parameters
        ----------
        value : str
            The value for the output variable.
        """
        self._vars[OUTPUT_VAR] = value

    def set_input(self, value: str) -> None:
        """Set the input variabel.

        Parameters
        ----------
        value : str
            The value for the input variable.
        """
        self._vars[INPUT_VAR] = value

    def set_set(self, value: str) -> None:
        """Set the set variabel.

        Parameters
        ----------
        value : str
            The value for the set variable.
        """
        self._vars[SET_VAR] = value

    def set_home(self, value: str) -> None:
        """Set the home variabel.

        Parameters
        ----------
        value : str
            The value for the home variable.
        """
        self._vars[HOME_VAR] = value

    def set_cpu(self, value: str) -> None:
        """Set the cpu variabel.

        Parameters
        ----------
        value : str
            The value for the cpu variable.
        """
        self._vars[CPU_VAR] = value

    def replace_vars(self, text: List[str]) -> List[str]:
        """Replace all variables in each line of text with the provided replacement string.

        Parameters
        ----------
        text : List[str]
            The text content line by line.
        variables : Variables
            The variables

        Returns
        -------
        List[str]
            The modified text content.
        """
        if not self._vars:
            return text
        for i, line in enumerate(text):
            for k, v in self._vars.items():
                try:
                    if k == SET_VAR:
                        # find parameter in brackets and modify value before replacement
                        indices = find_indices_of_substring(line, SET_VAR)
                        for index in indices:
                            subsequent = index + len(SET_VAR)
                            if not line[subsequent] == "[":
                                raise SyntaxError(
                                    f"Expected opening bracket [ after {SET_VAR} in line {i} at position {subsequent}."
                                )
                            end = line[subsequent:].find("]")
                            if end == -1:
                                raise SyntaxError(
                                    f"Expected closing bracket ] after {SET_VAR} in line {i} after position {subsequent}."
                                )
                            separator = line[subsequent + 1 : subsequent + end]
                            line = (
                                line[:index]
                                + separator.join(v)
                                + line[subsequent + end + 1 :]
                            )
                        text[i] = line
                    else:
                        text[i] = line.replace(k, v)
                except SyntaxError as e:
                    logging.error(e.msg)
        return text