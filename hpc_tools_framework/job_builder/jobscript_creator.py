import logging
from hpc_tools_framework.utils import Variables
from hpc_tools_framework.models import Jobscript
from hpc_tools_framework.job_builder import generate
from hpc_tools_framework.io import SSH, create_jobscript_file


def create_jobscript(ssh: SSH, jobscript: Jobscript, variables: Variables):
    """Generate the jobscript on the cluster.

    Parameters
    ----------
    ssh : SSH
        The ssh connection to the cluster.
    jobscript : Jobscript
        The jobscript to schedule.
    variables : Variables
        The variables to replace in the jobscript.
    """
    content = generate(jobscript)
    content = variables.replace_vars(content)
    create_jobscript_file(ssh, jobscript.name, content)
    logging.info(f"Created jobscript {jobscript.name}.")