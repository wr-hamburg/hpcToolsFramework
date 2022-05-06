import logging
from hpc_tools_framework.io import SSH
from hpc_tools_framework.utils import home_from_output


def tool_installation_dir(ssh: SSH, tool_name: str) -> str:
    """Return the installation path of the specified tool.

    Parameters
    ----------
    ssh : SSH
        The ssh connection.
    tool_name : str
        The tool name.

    Returns
    -------
    str
        The path.
    """
    # TODO check if tool installed
    output = ssh.run(f"spack find --path {tool_name.name}")
    output2 = "".join(output)
    if (
        f"Error: {tool_name} does not match any installed packages." in output2
        or f"No package matches the query: {tool_name}" in output2
    ):
        logging.error(f"{tool_name} is not installed. Trying to install it.")
        return None
    else:
        return home_from_output(output)