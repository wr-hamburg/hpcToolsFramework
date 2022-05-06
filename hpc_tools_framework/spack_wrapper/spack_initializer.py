import logging
from hpc_tools_framework.spack_wrapper import (
    SpackNotInstalledException,
)
from hpc_tools_framework.io import SSH
from hpc_tools_framework.constants import SPACK_GIT_REPO, TOOL_DIR
from hpc_tools_framework.utils import (
    clone_or_update,
)


def init_spack(ssh: SSH) -> None:
    """Check if Spack package manager is installed. Otherwise try to install it.

    Parameters
    ----------
    ssh : SSH
        The ssh connection to the server.

    Raises
    ------
    SpackNotInstalledException
        Is raised if Spack could not be installed.
    """
    clone_or_update(ssh, SPACK_GIT_REPO, TOOL_DIR)
    output = ssh.run("which spack")
    if not output:
        raise SpackNotInstalledException()
    ssh.run(f"source {TOOL_DIR}/spack/share/spack/setup-env.sh")
    logging.info("Setup spack.")