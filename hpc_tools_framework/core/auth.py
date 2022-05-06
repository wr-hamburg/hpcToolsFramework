import logging
from hpc_tools_framework.io import SSH, Server


def _login(cluster: str, username: str, password: str) -> SSH:
    """Log into the specified cluster with the provided credentials.

    Parameters
    ----------
    cluster : str
        The address of the cluster.
    username : str
        The username.
    password : str
        The password for the username.

    Returns
    -------
    SSH
        Returns the SSH connection object if the login was successful. Otherwise None.
    """
    server = Server(cluster, username, password)
    try:
        ssh = SSH(server)
        ssh.connect()
        ssh.open_shell()
        ssh._read_output()

        output = ssh.run("echo Login")
        if ["Login"] == output:
            logging.info(f"Login successful for {username} on {cluster}.")
            return ssh
    except:
        logging.error("Login unsuccessful.")
        return None


def _logout(ssh: SSH):
    """Logout from the cluster.

    Parameters
    ----------
    ssh : SSH
        The currently open ssh connection to the cluster.
    """
    ssh.close_shell()
    ssh.disconnect()
    logging.info("Logout successful.")