import ast
from typing import List
from hpc_tools_framework.models import Program, AnalysisJob, SlurmJobStatus
from hpc_tools_framework.io import SSH
from hpc_tools_framework.utils import (
    call_remote_function,
    url2dir,
    split_filepath,
)
from hpc_tools_framework.constants import TOOL_DIR, SCHEDULER_GIT_REPO


def insert_job(ssh: SSH, job: AnalysisJob) -> int:
    """Insert a job into the database.

    Parameters
    ----------
    ssh : SSH
        The ssh connection.
    job : AnalysisJob
        The job.

    Returns
    -------
    int
        The id for the job in the database.
    """
    # does the program already exist: yes -> get id, no -> insert program
    program = query_program_by_name(ssh, job.program_name)
    if program:
        program_id = program.id
    else:
        directory, _ = split_filepath(job.makefile_path)
        program_id = insert_program(
            ssh,
            Program(
                None,
                job.program_name,
                job.makefile_path,
                directory + "/" + job.program_name,
                directory,
            ),
        )

    output = call_remote_function(
        ssh,
        dir=f"{TOOL_DIR}/{url2dir(SCHEDULER_GIT_REPO)}",
        file="database_queries",
        function="insert_job",
        args=[
            job.timestamp_id,
            job.makefile_path,
            job.jobscript_path,
            job.status.name,
            program_id,
        ],
    )
    return int(output[0])


def insert_program(ssh: SSH, program: Program) -> int:
    """Insert a program into the database and return its id.

    Parameters
    ----------
    ssh : SSH
        The ssh connection to the cluster.
    program : Program
        The program to be inserted.

    Returns
    -------
    int
        The id of the inserted program.
    """
    output = call_remote_function(
        ssh,
        dir=f"{TOOL_DIR}/{url2dir(SCHEDULER_GIT_REPO)}",
        file="database_queries",
        function="insert_program",
        args=[
            program.name,
            program.makefile_path,
            program.program_path,
            program.directory,
        ],
    )
    # return the id of the program
    return int(output[0])


def query_program_by_name(ssh: SSH, program_name: str) -> Program:
    """Query a program by name in the database.

    Parameters
    ----------
    ssh : SSH
        The ssh connection.
    program_name : str
        The program name.

    Returns
    -------
    Program
        The program.
    """
    output = call_remote_function(
        ssh,
        dir=f"{TOOL_DIR}/{url2dir(SCHEDULER_GIT_REPO)}",
        file="database_queries",
        function="query_program_by_name",
        args=[program_name],
    )
    if output and output != [""]:
        params = ast.literal_eval(output[0])
        return Program(**params)
    else:
        return None


def query_programs(ssh: SSH) -> List[Program]:
    """Query all programs in the database.

    Parameters
    ----------
    ssh : SSH
        The ssh connection.

    Returns
    -------
    List[Program]
        A list of all programs in the database.
    """
    output = call_remote_function(
        ssh,
        dir=f"{TOOL_DIR}/{url2dir(SCHEDULER_GIT_REPO)}",
        file="database_queries",
        function="query_programs",
    )
    program_dicts = ast.literal_eval(output[0])
    return [Program(**params) for params in program_dicts]


def query_jobs_by_status(ssh: SSH, status: SlurmJobStatus) -> List[AnalysisJob]:
    """Query all jobs which are in the specified status.

    Parameters
    ----------
    ssh : SSH
        The ssh connection.
    status : SlurmJobStatus
        The status of a job.

    Returns
    -------
    List[AnalysisJob]
        A list of jobs.
    """
    output = call_remote_function(
        ssh,
        dir=f"{TOOL_DIR}/{url2dir(SCHEDULER_GIT_REPO)}",
        file="database_queries",
        function="query_jobs_by_status",
        args=[status],
    )
    job_dicts = ast.literal_eval(output[0])
    return [AnalysisJob(**params) for params in job_dicts]


def query_jobs_by_tool(ssh: SSH, toolname: str) -> List[AnalysisJob]:
    """Query jobs in the database by the tool that was applied.

    Parameters
    ----------
    ssh : SSH
        The ssh connection.
    toolname : str
        The name of the tool.

    Returns
    -------
    List[AnalysisJob]
        A list of jobs.
    """
    output = call_remote_function(
        ssh,
        dir=f"{TOOL_DIR}/{url2dir(SCHEDULER_GIT_REPO)}",
        file="database_queries",
        function="query_jobs_by_tool",
        args=[toolname],
    )
    job_dicts = ast.literal_eval(output[0])
    return [AnalysisJob(**params) for params in job_dicts]


def query_jobs(ssh: SSH) -> List[AnalysisJob]:
    """Query all jobs from the database.

    Parameters
    ----------
    ssh : SSH
        The ssh connection.

    Returns
    -------
    List[AnalysisJob]
        A list of all jobs in the database.
    """
    output = call_remote_function(
        ssh,
        dir=f"{TOOL_DIR}/{url2dir(SCHEDULER_GIT_REPO)}",
        file="database_queries",
        function="query_jobs",
    )
    job_dicts = ast.literal_eval(output[0])
    return [AnalysisJob(**params) for params in job_dicts]


def query_job_by_timestamp_id(ssh: SSH, timestamp_id: str) -> AnalysisJob:
    """Query a job by its timestamp id.

    Parameters
    ----------
    ssh : SSH
        The ssh connection.
    timestamp_id : str
        The timestamp id of the job.

    Returns
    -------
    AnalysisJob
        The job.
    """
    output = call_remote_function(
        ssh,
        dir=f"{TOOL_DIR}/{url2dir(SCHEDULER_GIT_REPO)}",
        file="database_queries",
        function="query_job_by_timestamp_id",
        args=[timestamp_id],
    )
    if output and output != [""]:
        params = ast.literal_eval(output[0])
        return AnalysisJob(**params)
    else:
        return None