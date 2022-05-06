import logging
from typing import List
from hpc_tools_framework.io import SSH, change_dir


def call_remote_function(
    ssh: SSH, dir: str, file: str, function: str, args: List[str] = None
) -> List[str]:
    """Calls a python function in the specified directory on the remote cluster.

    Parameters
    ----------
    ssh : SSH
        The ssh connection to the cluster.
    dir : str
        The directory which contains the python script.
    file : str
        The python script which contains the function.
    function : str
        The function.
    args : List[str], optional
        The arguments for the function.

    Returns
    -------
    List[str]
        The output of the python function, line by line.
    """
    change_dir(ssh, dir)
    if not args:
        args = list()
    arg_str = ""
    for i, arg in enumerate(args):
        if isinstance(arg, str):
            arg_str += f"'{arg}'"
        elif isinstance(arg, int):
            arg_str += f"{arg}"
        if i < len(args) - 1:
            arg_str += ", "
    command = f'python -c "import {file}; {file}.{function}({arg_str})"'
    output = ssh.run(command)
    change_dir(ssh, "~")
    logging.debug(f"RPC {file}.{function}: {output}")
    return output