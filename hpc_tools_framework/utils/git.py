"""Git related utility functions."""

import logging
from hpc_tools_framework.io import SSH, change_dir, dir_exists


def url2dir(url: str) -> str:
    """Extract the directory name from the git repo url.

    Parameters
    ----------
    url : str
        The git repo url.

    Returns
    -------
    str
        The directory name of the cloned repo.
    """
    return url.split("/")[-1][:-4]


def repo_exists(ssh: SSH, dir: str) -> bool:
    """Check if directory exists and is a git repository.

    Parameters
    ----------
    ssh : SSH
        The connection to the cluster.
    dir : str
        The directory path.

    Returns
    -------
    bool
        Returns whether the directory exists and is a git repository.
    """
    if not dir_exists(ssh, dir):
        return False
    output = ssh.run(f"git -C {dir} rev-parse")
    return not output


def update_repo(ssh: SSH, dir: str) -> bool:
    """Updates the git repo in the provided directory.

    Parameters
    ----------
    ssh : SSH
        The connection to the cluster.
    dir : str
        The directory of the git repo.

    Returns
    -------
    bool
        Returns whether an update was performed or not.
    """
    repo_name = dir.split("/")[-1]
    change_dir(ssh, dir)
    # make the repo pristine
    ssh.run("git reset --hard")
    # update the repo
    output = ssh.run("git pull")
    change_dir(ssh, "~")
    if output and output[0] == "Already up to date.":
        logging.info(f"Repo {repo_name} already up to date.")
        return False
    else:
        logging.info(f"Updated repo {repo_name}.")
        return True


def clone_repo(ssh: SSH, url: str, dir: str) -> None:
    """Clones the specified repository into the provided directory.

    Parameters
    ----------
    ssh : SSH
        The connection to the cluster.
    url : str
        The url of the repository to clone.
    dir : str
        The directory to clone the repo into.
    """
    change_dir(ssh, dir)
    # -c feature.manyFiles=true enables config options that optimize for repos with many files in the working directory
    # --depth 1 omits history
    ssh.run(f"git clone -c feature.manyFiles=true {url}")
    change_dir(ssh, "~")
    logging.info(f"Cloned repo {url}.")


def clone_or_update(ssh: SSH, url: str, dir: str):
    updated = False
    if repo_exists(ssh, f"{dir}/{url2dir(url)}"):
        updated = update_repo(ssh, f"{dir}/{url2dir(url)}")
    else:
        clone_repo(ssh, url, dir)
    return updated
