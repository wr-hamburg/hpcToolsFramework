from hpc_tools_framework.io import SSH
from typing import List


def list_dirs(ssh: SSH, dir: str = "~") -> List[str]:
    """Returns all directories on the server.

    Parameters
    ----------
    ssh : SSH
        The ssh connection to the server.
    dir : str, optional
        The directory to start listing subdirectories from, by default home.

    Returns
    -------
    List[str]
        A list of all subdirectories with their relative path to the specified directory.
    """
    ssh.run(f"cd {dir}")
    return ssh.run(f"ls -d */")


def dir_exists(ssh: SSH, dir: str) -> bool:
    exists = ssh.run(f"if [ -d '{dir}' ]; then echo 'True'; else echo 'False'; fi")
    if exists[0] == "True":
        return True
    elif exists[0] == "False":
        return False
    else:
        raise RuntimeError


def create_dir(ssh: SSH, dir: str) -> None:
    if dir_exists(ssh, dir):
        raise FileExistsError(f"Directory {dir} already exists.")
    ssh.run(f"mkdir {dir}")


def change_dir(ssh: SSH, dir: str) -> None:
    ssh.run(f"cd {dir}")