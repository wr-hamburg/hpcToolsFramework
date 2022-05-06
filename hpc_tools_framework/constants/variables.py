"""Defines the variables for the config files."""

OUTPUT_VAR = "§output"
"""The output directory variable for the HPC analysis tools."""

INPUT_VAR = "§input"
"""The input variable which makes the input string or number accessible."""

HOME_VAR = "§home"
"""The home variable which contains the installation path of a tool."""

CPU_VAR = "§cpu"
"""The cpu variable which contains the architecture of the login node."""

SET_VAR = "§set"
"""The set variable which makes the set of selected values accessible.
This variable is followed by a parameter containing the separator in brackets [] for the values.
For example to input a comma separated list of the selected values you need to write §set[,]."""