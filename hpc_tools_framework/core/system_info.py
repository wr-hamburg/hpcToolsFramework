from hpc_tools_framework.io import SSH


def system_cpu(ssh: SSH) -> str:
    """Return the cpu architecture of the login node of the cluster.

    Parameters
    ----------
    ssh : SSH
        The ssh connection to the cluster.

    Returns
    -------
    str
        The cpu architecture.
    """
    # TODO lookup os and select correct way to read cpu architecture
    output = ssh.run("uname -a")
    # TODO parse output
    return "x86_64"