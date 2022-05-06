from hpc_tools_framework.io import SSH, change_dir
from typing import List


def files_by_ext(
    ssh: SSH, ext: str, dir: str = "~", exclude_dirs: List[str] = list()
) -> List[str]:
    """Returns all files on the server with the specified extension.

    Parameters
    ----------
    ssh : SSH
        The ssh connection to the server.
    ext : str
        The extension of the files to search for.
    dir : str, optional
        The directory to start looking for files, by default home.
    exclude_dir : str
        The directories to exclude from the search.

    Returns
    -------
    List[str]
        A list of all file names with their relative path to the specified directory.
    """
    exclude_dirs.append("*/spack*")
    exclude_dirs = [f"'{dir}'" for dir in exclude_dirs]
    change_dir(ssh, dir)
    return ssh.run(
        f"find -type f -name '*.{ext}' {'-not -path ' + ' -not -path '.join(exclude_dirs)}"
    )


def file_exists(ssh: SSH, file: str) -> bool:
    """Checks whether the specified file exists.

    Parameters
    ----------
    ssh : SSH
        The ssh connection to the server.
    file : str
        The file to chech for.

    Returns
    -------
    bool
        [description]

    Raises
    ------
    RuntimeError
        [description]
    """
    exists = ssh.run(f"if [ -f '{file}' ]; then echo 'True'; else echo 'False'; fi")
    if exists[0] == "True":
        return True
    elif exists[0] == "False":
        return False
    else:
        raise RuntimeError


def read_file(ssh: SSH, file: str) -> List[str]:
    """Returns the content of the specified file.

    Parameters
    ----------
    ssh : SSH
        The ssh connection to the server.
    file : str
        The file which content to read from.

    Returns
    -------
    List[str]
        The content of the specified file as a list of lines.

    Raises
    ------
    FileNotFoundError
        Is raised if the specified file does not exist.
    """
    if not file_exists(ssh, file):
        raise FileNotFoundError
    return ssh.run(f"cat {file}")


def write_file(ssh: SSH, file: str, content: List[str]) -> None:
    """Write the content line by line into the specified file.

    Parameters
    ----------
    ssh : SSH
        The ssh connection to the server.
    file : str
        The file to write the content to.
    content : List[str]
        The content to write into the file.

    Raises
    ------
    FileNotFoundError
        Is raised if the specified file does not exist.
    ValueError
        Is raised if the provided content is empty.
    """
    if not file_exists(ssh, file):
        raise FileNotFoundError
    if not content:
        raise ValueError(content)
    ssh.run(f"echo '{content[0]}' > {file}")
    if len(content) > 1:
        for line in content[1:]:
            ssh.run(f"echo '{line}' >> {file}")


def create_file(ssh: SSH, file: str, content: str = None) -> None:
    """Creates the specified file and optionally writes the provided content into it.

    Parameters
    ----------
    ssh : SSH
        The ssh connection to the server.
    file : str
        The file to create.
    content : str, optional
        The content to write into the specified file, by default None.

    Raises
    ------
    FileExistsError
        Is raised if the specified file already exists.
    """
    if file_exists(ssh, file):
        raise FileExistsError
    ssh.run(f"touch {file}")
    if content:
        write_file(ssh, file, content)


def copy_file(ssh: SSH, file: str, new_file: str) -> None:
    ssh.run(f"cp {file} {new_file}")