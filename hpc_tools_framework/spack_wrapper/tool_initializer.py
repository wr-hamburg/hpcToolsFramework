from hpc_tools_framework.models import ToolInstallation
from hpc_tools_framework.io import SSH
from hpc_tools_framework.utils import home_from_output
import logging


def install_tool(
    ssh: SSH, tool_name: str, installation: ToolInstallation = None
) -> None:
    """Installs the specified tool with the spack package manager on the cluster.

    Parameters
    ----------
    ssh : SSH
        The ssh connection to the cluster.
    tool_name : str
        The name of the tool.
    installation : ToolInstallation
        The installation settings of the tool.

    Raises
    ------
    ValueError
        Is raised if the tool does not exist in spack or failed to install.
    """
    installation_string = tool_name
    if installation:
        if installation.version:
            installation_string += f"@{installation.version}"
        for flag in installation.flags:
            installation_string += f"{flag.prefix}{flag.value}@{flag.suffix}"
    try:
        output = ssh.run(f"spack install {installation_string}")
    except Exception as e:
        # TODO sometimes spack fails to install a tool
        logging.error(e)
    output = "".join(output)
    # outputs have changed during the development and might change again
    logging.debug(output)
    if "==> Error:" in output:
        raise ValueError(f"{tool_name} does not exist in spack.")
    if not "Successfully installed" in output:
        raise ValueError(f"{tool_name} failed to install.")


def init_tool(ssh: SSH, tool_name: str, installation: ToolInstallation = None) -> str:
    """Initializes the specified tool on the cluster.

    Parameters
    ----------
    ssh : SSH
        The ssh connection to the cluster.
    tool_name : str
        The name of the tool.
    installation : ToolInstallation
        The installation settings of the tool.

    Raises
    ------
    ValueError
        Is raised if the tool does not exist in spack or failed to install.

    Returns
    -------
    str
        The installation directory of the tool.
    """
    # TODO check whether version in installation is the same as the installed version
    output = ssh.run(f"spack find --path {tool_name}")
    joined_output = "".join(output)
    if (
        f"Error: {tool_name} does not match any installed packages." in joined_output
        or f"No package matches the query: {tool_name}" in joined_output
    ):
        logging.error(f"{tool_name} is not installed. Trying to install it.")
        install_tool(ssh, tool_name, installation)
    # TODO so far we pick the last package only and maybe want to be more specific
    # look into the function home_from_output for more details
    installation_dir = home_from_output(output)
    package_hash = installation_dir.split("-")[-1]
    if len(output) == 2:
        ssh.run(f"spack load {tool_name}")
        logging.info(f"Initialized tool {tool_name}.")
    else:
        ssh.run(f"spack load /{package_hash}")
        logging.info(f"Initialized tool {tool_name} from package {package_hash}.")
    return installation_dir