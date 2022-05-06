import logging

from hpc_tools_framework.utils import split_filepath
from hpc_tools_framework.io import SSH, change_dir


def remove_object_files(ssh: SSH, makefile_path: str) -> None:
    """Clean all object files in the specified directory of the makefile.

    Parameters
    ----------
    ssh : SSH
        The ssh connection to the cluster.
    makefile_path : str
        The path to the Makefile.
    """
    path, _ = split_filepath(makefile_path)
    change_dir(ssh, path)
    ssh.run("make clean")
    change_dir(ssh, "~")
    logging.info(f"Cleaned all object files in: {path}")
