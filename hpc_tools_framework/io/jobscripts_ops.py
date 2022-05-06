from hpc_tools_framework.io import SSH, create_file
from hpc_tools_framework.constants import TOOL_DIR, JOBSCRIPT_DIR


def create_jobscript_file(ssh: SSH, file: str, content: str) -> None:
    """Create a jobscript file in the dedicated jobscript folder.

    Parameters
    ----------
    ssh : SSH
        The ssh connection to the server.
    file : str
        The name of the jobscript file.
    content : str
        The content of the jobscript file.
    """
    create_file(ssh, f"{TOOL_DIR}/{JOBSCRIPT_DIR}/{file}", content)