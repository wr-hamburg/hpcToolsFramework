from hpc_tools_framework.io import SSH


def add_cronjob(ssh: SSH, cmd: str, period: str):
    """Add a cron job to the cluster.

    Parameters
    ----------
    ssh : SSH
        The ssh connection.
    cmd : str
        The command to be executed.
    period : str
        The execution period pf the cron job.
    """
    ssh.run(f'( crontab -l | grep -v -F "{cmd}" ; echo "{period} {cmd}" ) | crontab -')


def remove_cronjob(ssh: SSH, cmd: str):
    """Remove a cron job from the cluster.

    Parameters
    ----------
    ssh : SSH
        The connection to the cluster.
    cmd : str
        The command of the cron job to be removed.
    """
    ssh.run(f'( crontab -l | grep -v -F "{cmd}" ) | crontab -')