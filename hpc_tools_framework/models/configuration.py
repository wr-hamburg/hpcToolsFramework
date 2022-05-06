from dataclasses import dataclass
from typing import List
from hpc_tools_framework.models import MailType, SettingType, Program


@dataclass
class JobConfiguration:
    """The user specific configurations for the jobscript."""

    minnodes: int
    """The minimum number of allocated nodes."""
    task_number: int
    """The number of allocated tasks."""
    partition: str
    """The name of the partition to run the job on."""
    processes: int
    """The number of processes."""
    source: str
    """The source string."""
    cp: str
    """The cp string."""
    memory: str
    """The allocated memory limit."""
    timeout: int = None
    """The timeout of the job in seconds."""
    mail_notifications: List[MailType] = None
    """The prefered mail notifications."""
    maxnodes: int = None
    """Optional maximum number of nodes allocated to this job. If it is not explicitly set, the maximum number of nodes is equal to the minimum."""


@dataclass
class SettingConfiguration:
    """Contains the values and the type for a specific setting of a tool."""

    name: str
    """The name of the setting. This string has to match with the name property in the ToolSetting class."""
    type: SettingType
    """The type of the setting. The type becomes relevant in how to process the values of the setting."""
    values: List[str] = None
    """The values of the setting. These are only relevant for the Input and Set setting."""


@dataclass
class ToolConfiguration:
    """Contains all settings for a specific tool that should be used to analyze a program."""

    name: str
    """The name of the tool. This string has to match with the name property in the Tool class."""
    settings: List[SettingConfiguration]
    """The settings for the tool."""


@dataclass
class ProgramConfiguration:
    """Contains all configurations for the program."""

    program: Program
    """The program."""
    execution_params: str
    """The execution parameters for the program."""


@dataclass
class Configuration:
    """Contains all configurations from the frontend."""

    job_config: JobConfiguration
    """The user specific configurations for the jobscript."""
    tools: List[ToolConfiguration]
    """Contains all settings for a specific tool that should be used to analyze a program."""
    program_config: ProgramConfiguration
    """The program configuration."""
