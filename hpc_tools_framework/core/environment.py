import logging
from hpc_tools_framework.io import SSH, dir_exists, create_dir
from hpc_tools_framework.constants import (
    TOOL_DIR,
    JOBSCRIPT_DIR,
    JOBSCRIPT_OUTPUT_DIR,
    JOBSCRIPT_CHECKPOINT_DIR,
    OUTPUT_DIR,
    INPUT_DIR,
    DATABASE_DIR,
    REPORT_DIR,
)


def _create_dir(ssh: SSH, dir) -> None:
    if not dir_exists(ssh, dir):
        create_dir(ssh, dir)
        logging.info(f"Created {dir} because it did not exist yet.")


def init_environment(ssh: SSH) -> None:
    """Initializes the environment folders for the tool.

    Parameters
    ----------
    ssh : SSH
        The ssh connection to the cluster.
    """
    _create_dir(ssh, TOOL_DIR)
    _create_dir(ssh, f"{TOOL_DIR}/{JOBSCRIPT_DIR}")
    _create_dir(ssh, f"{TOOL_DIR}/{JOBSCRIPT_OUTPUT_DIR}")
    _create_dir(ssh, f"{TOOL_DIR}/{OUTPUT_DIR}")
    _create_dir(ssh, f"{TOOL_DIR}/{JOBSCRIPT_CHECKPOINT_DIR}")
    _create_dir(ssh, f"{TOOL_DIR}/{INPUT_DIR}")
    _create_dir(ssh, f"{TOOL_DIR}/{DATABASE_DIR}")
    _create_dir(ssh, f"{TOOL_DIR}/{REPORT_DIR}")
