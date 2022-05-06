import logging
from typing import List
from hpc_tools_framework.io import SSH
from hpc_tools_framework.constants import TOOL_DIR, INPUT_DIR


def upload_input_file(ssh: SSH, file_path: str) -> None:
    file_name = file_path.split("/")[-1]
    try:
        ssh.upload(file_path, f"{TOOL_DIR}/{INPUT_DIR}/{file_name}")
    except FileNotFoundError as e:
        logging.error(e)
    except FileExistsError as e:
        logging.error(e)


def delete_input_file(ssh: SSH, file_name: str) -> None:
    """Delete a file in the input directory.

    Parameters
    ----------
    ssh : SSH
        The ssh connection to the cluster.
    file_name : str
        The name of the file inside the input directory.
    """
    ssh.run(f"rm {TOOL_DIR}/{INPUT_DIR}/{file_name}")


def input_files(ssh: SSH) -> List[str]:
    """Return a list of all input files uploaded to the cluster.

    Parameters
    ----------
    ssh : SSH
        The ssh connection to the cluster.

    Returns
    -------
    List[str]
        A list of all uploaded input files.
    """
    output = ssh.run(f"ls {TOOL_DIR}/{INPUT_DIR}")
    return output