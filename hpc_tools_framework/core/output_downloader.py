from typing import List

from hpc_tools_framework.io import SSH
from hpc_tools_framework.scheduler import query_job_by_timestamp_id
from hpc_tools_framework.models import SlurmJobStatus
from hpc_tools_framework.constants import TOOL_DIR, INPUT_DIR


def download_outputs(ssh: SSH, job_ids: List[str], database_works: bool) -> None:
    """Download the outputs for the jobs with the specified timestamp ids.

    Parameters
    ----------
    ssh : SSH
        The ssh connection.
    job_ids : List[str]
        The timestamp ids of the jobs.
    database_works : bool
        Bool which tells whether the database works.
    """
    for job_id in job_ids:
        if database_works:
            job = query_job_by_timestamp_id(ssh, job_id)
            if job and job.status == SlurmJobStatus.Finished:
                # TODO is this the correct path to the output file?
                # And maybe we rather want to support directories too
                ssh.download_file(f"{TOOL_DIR}/{INPUT_DIR}/job_id")