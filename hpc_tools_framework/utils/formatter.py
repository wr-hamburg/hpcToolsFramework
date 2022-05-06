from datetime import datetime
import logging
import time


def time_string(timestamp: datetime) -> str:
    """Generates a timestring from the given timestamp.

    Parameters
    ----------
    timestamp : datetime
        A timestamp.

    Returns
    -------
    str
        A string which represents the datetime.
    """
    time_str = time.strftime("%Y%m%d%H%M%S".format(timestamp))
    time_str += f"{timestamp.microsecond}".zfill(6)
    return time_str


def home_from_output(output: str) -> str:
    """Extract the installation directory of the output from the spack find command.

    Parameters
    ----------
    output : str
        The output string.

    Returns
    -------
    str
        The installation directory.
    """
    if len(output) < 2:
        logging.error(
            f"The output has a format which is not supported to extract the installation directory of the package: {output}"
        )
    package_rows = output[1:]
    packages = [row.split()[-1][1:] for row in package_rows]
    # TODO so far we select the last package but we might want to be more specific
    return packages[-1]
