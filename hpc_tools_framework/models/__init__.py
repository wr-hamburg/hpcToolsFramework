"""The models module."""

from hpc_tools_framework.models.slurm_job_status import SlurmJobStatus
from hpc_tools_framework.models.tool import (
    Tool,
    ToolInstallation,
    ToolCompiler,
    InstallationFlag,
    SingleEnvVar,
    ListedEnvVar,
    ToolJob,
    ToolSetting,
    SettingType,
    ToolOutput,
    OutputType,
)
from hpc_tools_framework.models.jobscript import Jobscript, MailType
from hpc_tools_framework.models.program import Program
from hpc_tools_framework.models.configuration import (
    Configuration,
    JobConfiguration,
    ToolConfiguration,
    SettingConfiguration,
    ProgramConfiguration,
)
from hpc_tools_framework.models.analysis import AnalysisJob
from hpc_tools_framework.models.compiler_level import CompilerLevel
from hpc_tools_framework.models.cluster_info import ClusterInfo, Partition

__all__ = [
    "SlurmJobStatus",
    "Tool",
    "ToolInstallation",
    "ToolCompiler",
    "InstallationFlag",
    "SingleEnvVar",
    "ListedEnvVar",
    "ToolJob",
    "ToolSetting",
    "Jobscript",
    "MailType",
    "Configuration",
    "JobConfiguration",
    "SettingType",
    "ToolConfiguration",
    "SettingConfiguration",
    "ProgramConfiguration",
    "ToolOutput",
    "OutputType",
    "Program",
    "AnalysisJob",
    "CompilerLevel",
    "ClusterInfo",
    "Partition",
]
