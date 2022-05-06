from hpc_tools_framework.utils import split_filepath
from hpc_tools_framework.io import file_exists, SSH
from hpc_tools_framework.models import Program


def _program_by_path(ssh: SSH, program_path: str) -> Program:
    """Return a program object for the specified program path.

    Parameters
    ----------
    program_path : str
        The path to the program.

    Returns
    -------
    Program
        A program object.
    """
    directory, name = split_filepath(program_path)
    makefile_path = directory + "/Makefile"
    if not file_exists(ssh, makefile_path):
        raise FileNotFoundError(
            f"The specified program {program_path} has no Makefile."
        )
    return Program(
        id=None,
        name=name,
        makefile_path=makefile_path,
        program_path=program_path,
        directory=directory,
    )
