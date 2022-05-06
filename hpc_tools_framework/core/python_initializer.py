import logging

from hpc_tools_framework.io.dir_ops import dir_exists

from hpc_tools_framework.constants import TOOL_DIR, PYTHON_LOCAL
from hpc_tools_framework.io import change_dir
from hpc_tools_framework.io import SSH
from hpc_tools_framework.spack_wrapper import init_tool


def init_python(ssh: SSH):
    """_summary_

    Parameters
    ----------
    ssh : SSH
        _description_
    """
    change_dir(ssh, TOOL_DIR)
    if not dir_exists(ssh, PYTHON_LOCAL):
        init_tool(ssh, "python")
        ssh.run(f"python -m venv {PYTHON_LOCAL}")
        logging.info("Created local python environment.")
    ssh.run(f"source ./{PYTHON_LOCAL}/bin/activate")
    logging.info("Activated local python environment.")
    # pip update
    ssh.run("pip install --upgrade pip")
    logging.info("Upgraded pip.")
    change_dir(ssh, "~")
