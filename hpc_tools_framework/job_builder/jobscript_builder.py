from datetime import datetime

from hpc_tools_framework.models import (
    Jobscript,
    ToolJob,
    JobConfiguration,
    ProgramConfiguration,
    ToolConfiguration,
)
from hpc_tools_framework.utils import time_string


def build_jobscripts(
    job: ToolJob,
    job_config: JobConfiguration,
    timestamp: datetime,
    tool_config: ToolConfiguration,
    program_config: ProgramConfiguration,
) -> Jobscript:
    """Builds a jobscript object from the provided information.

    Parameters
    ----------
    job : ToolJob
        The specific job settings for the applied tool.
    job_config : JobConfiguration
        The job settings selected by the user.
    timestamp : datetime
        The timestamp to identify the jobscript.
    tool_config : ToolConfiguration
        The cofiguration for the analysis tool which is used for the program telemetry.
    program_config : str
        The program and its execution parameters.

    Returns
    -------
    Jobscript
        Returns a jobscript object.
    """

    executable_string = (
        "../../"
        + program_config.program.program_path
        + " "
        + program_config.execution_params
    )

    return Jobscript(
        date=timestamp,
        name=f"jobscript.{time_string(timestamp)}",
        minnodes=job_config.minnodes,
        maxnodes=job_config.maxnodes,
        ntasks=job_config.task_number,
        timeout=job_config.timeout,
        partition=job_config.partition,
        processes=job_config.processes,
        source=job.source,
        cp=job.cp,
        # the program path is relative to home dir but the jobscript is called from inside the jobscript output directory
        executable_string=executable_string,
        single_env_variables=job.single_env_variables,
        listed_env_variables=job.listed_env_variables,
        pre_mpi_commands=job.pre_mpi_command,
        post_mpi_commands=job.post_mpi_command,
        post_binary_flags=job.post_binary_flags,
        memory=job_config.memory,
        tool_name=tool_config.name,
        mail_notifications=job_config.mail_notifications,
    )