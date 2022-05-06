from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from hpc_tools_framework.models import (
    JobConfiguration,
    ToolConfiguration,
    SlurmJobStatus,
)


@dataclass
class AnalysisJob:
    """Represents an analysis job."""

    id: int
    """The id in the database."""
    timestamp_id: str
    """The unique identifier of the analysis job."""
    status: SlurmJobStatus
    """The status of the job."""
    program_name: str
    """The name of the program which is analysed."""
    job_config: JobConfiguration
    """The configuration of the job."""
    tool_config: ToolConfiguration
    """The configuration of the analysis tool."""
    makefile_path: str
    """The path to the makefile for building the program."""
    jobscript_path: str
    """The path to the jobscript."""
    jobscript_ouput_path: str
    """The path to the jobscript output file."""
    jobscript_ouput_error_path: str
    """The path to the jobscript output error file."""
    tool_output_path: str
    """The path to the tool output."""
    created: datetime
    """The timestamp when the analysis job was created."""
    scheduled_time: datetime
    """The timestamp when the analysis job was scheduled."""
    started_time: datetime
    """The timestamp when the analysis job was started."""
    finished_time: datetime
    """The timestamp when the analyis job finished."""
