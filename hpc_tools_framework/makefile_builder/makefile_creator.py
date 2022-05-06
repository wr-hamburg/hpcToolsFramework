from datetime import datetime
import logging
from hpc_tools_framework.models import ToolCompiler
from hpc_tools_framework.makefile_builder import modify_makefile
from hpc_tools_framework.io import SSH, read_file, create_file, copy_file, change_dir
from hpc_tools_framework.utils import time_string, Variables, split_filepath


def create_makefile(
    ssh: SSH,
    makefile_path: str,
    variables: Variables,
    timestamp: datetime = None,
    tool_compiler: ToolCompiler = None,
) -> str:
    """Create the Makefile with the provided compiler params for the specified analysis tool on the cluster.

    Parameters
    ----------
    ssh : SSH
        The ssh connection to the cluster.
    makefile_path : str
        The path to the Makefile.
    variables : Variables
        The variables to replace in the modified makefile.
    timestamp : datetime
        The timestamp to identify the Makefile.
    tool_compiler : ToolCompiler
        The compiler params for the analysis tool.

    Raises
    ------
    ValueError
        Raised if specified makefile does not exist.

    Returns
    -------
    str
        The Makefile path.
    """
    path, filename = split_filepath(makefile_path)
    change_dir(ssh, path)
    # append timestamp at the end of the generated filename
    if timestamp:
        new_filename = f"{filename}.{time_string(timestamp)}"
    else:
        new_filename = filename

    if tool_compiler:
        makefile = read_file(ssh, filename)
        new_makefile = modify_makefile(makefile, tool_compiler)
        new_makefile = variables.replace_vars(new_makefile)
        create_file(ssh, new_filename, new_makefile)
    else:
        # if there is no need to modify the makefile we can just rename a copy of the original
        copy_file(ssh, filename, new_filename)
    change_dir(ssh, "~")
    logging.info(f"Created Makefile {new_filename}.")
    return path + "/" + new_filename
