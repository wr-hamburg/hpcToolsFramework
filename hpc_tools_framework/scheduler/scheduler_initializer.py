import logging

from hpc_tools_framework.scheduler import DatabaseException
from hpc_tools_framework.io import SSH, file_exists
from hpc_tools_framework.utils import (
    url2dir,
    call_remote_function,
    add_cronjob,
    clone_or_update,
)
from hpc_tools_framework.spack_wrapper import init_tool
from hpc_tools_framework.constants import (
    TOOL_DIR,
    POSTGRES_NAME,
    SCHEDULER_GIT_REPO,
    WATCHER_PERIOD,
    DATABASE_DIR,
)


def init_database(ssh: SSH) -> None:
    """Initilize the database and all needed tables for the analysis jobs.

    Parameters
    ----------
    ssh : SSH
        The ssh connection to the cluster.
    user : str
        The cluster user.
    """

    init_tool(ssh, POSTGRES_NAME)

    output = call_remote_function(
        ssh,
        f"{TOOL_DIR}/{url2dir(SCHEDULER_GIT_REPO)}",
        "database_initializer",
        "init_database",
    )
    if any([msg.startswith("ERROR") for msg in output]):
        raise DatabaseException(
            "Could not initialize database. See the output from the cluster for more details:",
            output,
        )
    logging.info("Initialized database.")


def init_watcher(ssh: SSH) -> None:
    """Initializes the watcher on the cluster and creates a cron job which schedules its periodical execution.

    Parameters
    ----------
    ssh : SSH
        The ssh connection to the cluster.
    """
    # create cron job
    cmd = f"/home/{ssh.user}/{TOOL_DIR}/{url2dir(SCHEDULER_GIT_REPO)}/watcher.sh"
    add_cronjob(ssh, cmd, WATCHER_PERIOD)
    logging.info("Initialized watcher.")


def init_scheduler(ssh: SSH):
    """Initializes the scheduler.

    Parameters
    ----------
    ssh : SSH
        The ssh connection to the cluster.
    """
    updated = clone_or_update(ssh, SCHEDULER_GIT_REPO, TOOL_DIR)
    # if updated:
    #     # TODO migrate data from database instead of deleting everything
    #     # shutdown database first
    #     ssh.run(f"pg_ctl stop -D {TOOL_DIR}/{DATABASE_DIR}/")
    #     logging.info("Shutdown database server.")
    #     # empty database directory
    #     ssh.run(f"rm -rf {TOOL_DIR}/{DATABASE_DIR}/*")
    #     logging.info("Deleted whole database.")

    # install necessary pip packages
    requirements_file = f"{TOOL_DIR}/{url2dir(SCHEDULER_GIT_REPO)}/requirements.txt"
    if file_exists(ssh, requirements_file):
        ssh.run(f"pip install -r {requirements_file}")

    init_database(ssh)
    init_watcher(ssh)