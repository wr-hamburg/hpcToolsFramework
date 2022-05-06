from dataclasses import dataclass
from enum import Enum
from typing import List


@dataclass
class ToolCompiler:
    """All aspects of the program under investigation related to the compiler and expressed in a standardized Makefile."""

    compiler: str = None
    """The compiler string to be used at CC. May also be used for prefixes (scorep mpicc instead of mpicc) or wrapper (tau_cc.sh instead of mpicc)
    """
    cflags: List[str] = None
    """Compiler flags to be used.
    """
    libs: List[str] = None
    """Libraries to be included
    """
    include_link: str = None
    """Include link to be used with the -I flag.
    """
    library_link: str = None
    """Library link to be used with the -L flag.
    """
    compiler_level: str = None
    """Compiler level if specified. Can be empty otherwise and the default level specified in the Makefile will be used.
    """


@dataclass
class SingleEnvVar:
    """Environmental variables to be applied in the jobscript. Will be included in the form export VARIABLE_NAME = VARIABLE_VALUE."""

    name: str
    """Identifier of the variable.
    """
    value: str
    """Value of the variable.
    """


@dataclass
class ListedEnvVar:
    """Environmental variables to be applied in the jobscript and have multiple, listed values which can be applied. Will be included in the form export VARIABLE_NAME = VARIABLE_VALUE1, VARIABLE_VALU2 ...."""

    name: str
    """Identifier of the variable.
    """
    values: List[str]
    """Values of the variable which will be listed as values.
    """
    separator: str
    """Seperator between the values. Might be different between each tool.
    """


@dataclass
class ToolJob:
    """All aspects of the program under investigation related to the job script and execution."""

    single_env_variables: List[SingleEnvVar] = None
    """All environmental variables which have to be set.
    """
    listed_env_variables: List[ListedEnvVar] = None
    """All environmental variables which have to be set and have multiple, listed values.
    """
    pre_mpi_command: List[str] = None
    """All commands/strings which have to be listed before the MPI command (mpirun / mpiexec).
    """
    post_mpi_command: List[str] = None
    """All commands/strings which have to be listed after the MPI command (mpirun / mpiexec).
    """
    post_binary_flags: List[str] = None
    """All commands/strings which have to be listed after the executable.
    """
    cp: str = None
    """Cp command in the jobscript for copy data (like in Extrae).
    """
    source: str = None
    """Sourcing commands for the execution.
    """


@dataclass
class InstallationFlag:
    """Flags to use behind the spack install command."""

    name: str
    """Name of the flag. Can be choosen free.
    """
    value: str
    """value of the flag to be applied behind the spack install command.
    """
    prefix: str = None
    """Prefix of the flag value (like + or -).
    """
    suffix: str = None
    """Suffix of the flag value (like versions in the form @1.11.9).
    """


@dataclass
class ToolInstallation:
    """All aspects of the program under investigation related to the installation and spack handling."""

    version: str = None
    """Version of the tool. Can be left empty.
    """
    flags: List[InstallationFlag] = None
    """List of lfags to be applied behind the installation command. 
    """


class SettingType(Enum):
    """The type of a setting.
    Settings for tools are flags which represent either a bool,
    add another input value to the execution or a whole set of values.
    """

    Bool = 0
    """A bool input like [true]. This type of setting is represented as a checkbox in the UI."""
    Textinput = 1
    """A text input like ["./path/a/b"]. This type of setting is represented as a textfield in the UI."""
    Numberinput = 2
    """A number input like [12]. This type of setting is represented as a numberfield in the UI."""
    Set = 3
    """A set of values like ["PAPI_FP_OPS", "PAPI_L2_TCM"].  This type of setting is represented as a multiselect dropdown in the UI."""
    File = 4
    """Files in the input directory. This type of setting is represented as a dropdown with all input files in the UI."""


class OutputType(Enum):
    """Output types which indicates how the output is generated."""

    Jobscript_Output = 0
    """The output can be collected in the jobscript output file."""


@dataclass
class ToolOutput:
    """All aspects of the program under investigation related to the installation and the output and UI presentation."""

    type: OutputType
    """Output type which than gives the backend information for further processing. 
    """


@dataclass
class ToolSetting:
    """Tool class settings."""

    name: str
    """Name of the setting.
    """
    type: SettingType
    """Type of the setting.
    """
    description: str
    """Setting description for the UI.
    """
    values: List[str] = None
    """All values for the setting which can also be a list where the user can pick settings. 
    """
    compiler: ToolCompiler = None
    """Compiler settings which have to be applied in order to use the setting. Can be left empty to use the tool default.
    """
    job: ToolJob = None
    """Job settings which have to be applied in order to use the setting. Can be left empty to use the tool default.
    """
    installation: ToolInstallation = None
    """Installation settings which have to be applied in order to use the setting. Can be left empty to use the tool default.
    """


@dataclass
class Tool:
    """Tool class with all values and settings as list."""

    title: str
    """Title of the tool.
    """
    fulltitle: str
    """Full title of the tool without abbreviation.
    """
    url: str
    """Tool homepage.
    """
    name: str
    """Name of the tool in Spack / APT.
    """
    description: str
    """Short description of the tool for the UI.
    """
    compiler: ToolCompiler
    """Default compiler settings.
    """
    job: ToolJob
    """Default job settings.
    """
    installation: ToolInstallation
    """Default installation settings.
    """
    output: ToolOutput
    """Output type and descriptor.
    """
    settings: List[ToolSetting]
    """List of all settings for the user to choose from. 
    """
