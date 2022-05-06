from hpc_tools_framework.utils import split_filepath
from hpc_tools_framework.models import Program
from hpc_tools_framework.io import SSH, change_dir, read_file
from typing import List
import re


def targets_from_makefile(makefile: List[str]) -> List[str]:
    """Returns all targets of the makefile.

    Parameters
    ----------
    makefile : List[str]
        The makefile where each line is an element in the list.

    Returns
    -------
    List[str]
        The targets of the makefile listed after the 'all:' keyword.

    Raises
    ------
    ValueError
        The provided makefile does not specify a target with the all keyword.
    """
    for line in makefile:
        if line.startswith("all:"):
            targets = line[4:].lstrip().split(" ")
    if targets:
        return targets
    else:
        raise ValueError(
            "The provided makefile does not specify a target with the 'all' keyword."
        )


generated_makefile_pattern = re.compile("(M|m)akefile(\w|\.)*\.\d{20}")
"""This is the regex to match the generated Makefile file names."""


def list_makefiles(
    ssh: SSH, dir: str = "~", exclude_dirs: List[str] = list()
) -> List[str]:
    """Returns all Makefiles on the server.

    Parameters
    ----------
    ssh : SSH
        The ssh connection to the server.
    dir : str, optional
        The directory to start looking for Makefiles, by default home.
    exclude_dirs : List[str]
        The directories to exclude from the search.

    Returns
    -------
    List[str]
        A list of all Makefiles with their relative path to the specified directory.
    """
    exclude_dirs.append("*/spack*")
    exclude_dirs = [f"'{dir}'" for dir in exclude_dirs]
    change_dir(ssh, dir)
    makefiles = ssh.run(
        f"find -type f -iname 'Makefile*' {'-not -path ' + ' -not -path '.join(exclude_dirs)}"
    )
    # filter out all generated makefiles
    makefiles = list(
        filter(
            lambda x: not bool(generated_makefile_pattern.match(x.split("/")[-1])),
            makefiles,
        )
    )
    # remove ./ at the beginning of the paths
    return list(map(lambda x: x[2:], makefiles))


def programs_by_makefiles(ssh: SSH, dir: str = "~") -> List[Program]:
    """Return a list of all programs and their paths of the makefiles on the server

    Parameters
    ----------
    ssh : SSH
        The ssh connection to the server.
    dir : str, optional
        The directory to start looking for makefiles, by default home.

    Returns
    -------
    List[Program]
        A list of all programs with their paths of their makefiles.
    """
    makefile_paths = list_makefiles(ssh, dir)
    programs = list()
    for makefile_path in makefile_paths:
        try:
            makefile = read_file(ssh, makefile_path)
            targets = targets_from_makefile(makefile)
            if len(targets) == 1:
                program_name = targets[0]
                directory, _ = split_filepath(makefile_path)
                # remove ./ at the beginning
                if directory.startswith("./"):
                    directory = directory[2:]
                program_path = directory + "/" + program_name
                programs.append(
                    Program(
                        id=None,
                        name=program_name,
                        makefile_path=makefile_path,
                        program_path=program_path,
                        directory=directory,
                    )
                )
        except:
            pass
        return programs