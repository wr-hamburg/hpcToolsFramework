import logging
from typing import List
from hpc_tools_framework.models.cluster_info import ClusterInfo
from hpc_tools_framework.io import (
    SSH,
    programs_by_makefiles,
    _program_by_path,
)
from hpc_tools_framework.utils import (
    Variables,
)
from hpc_tools_framework.models import (
    Configuration,
    Program,
    AnalysisJob,
    SlurmJobStatus,
)
from hpc_tools_framework.core import (
    load_configs,
    init_environment,
    slurm_info,
    run_pipeline,
    upload_input_file,
    input_files,
    init_python,
    download_outputs,
)
from hpc_tools_framework.core.auth import _login, _logout
from hpc_tools_framework.spack_wrapper import init_spack
from hpc_tools_framework.scheduler import (
    init_scheduler,
    query_jobs_by_status,
    query_jobs_by_tool,
    query_jobs,
    DatabaseException,
)


class Core:
    """The core class which bundles and provides all functionality for the frontend or a possible CLI."""

    def __init__(self):
        """Constructor of the core class."""
        self.tools = load_configs()
        """The list of supported tools and their settings."""
        self.ssh = None
        """The ssh connection."""
        self.init_done = False
        """Tells whether the initialization process is finished or not."""
        self.database_works = False
        """Tells whether the initialization of the database was successful."""

    def init_cluster(self) -> None:
        """Initialize all dependencies on the cluster."""
        init_environment(self.ssh)
        init_spack(self.ssh)
        init_python(self.ssh)
        try:
            init_scheduler(self.ssh)
            self.database_works = True
        except DatabaseException as e:
            self.database_works = False
            logging.error(e)
        self.init_done = True
        logging.info("Finished initialization.")

    def login(self, cluster: str, username: str, password: str) -> bool:
        """Log into the specified cluster with the provided credentials.
        After a successful login, spack is initialized.

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
        bool
            Returns whether the login was successful or not.
        """
        ssh = _login(cluster, username, password)
        if ssh:
            # login succussful
            self.ssh = ssh
            return True
        else:
            # login unsuccessful
            return False

    def logout(self) -> bool:
        """Logout from the cluster.

        Returns
        -------
        bool
            Returns whether the logout was successful or not.
        """
        if self.ssh:
            _logout(self.ssh)
            return True
        else:
            return False

    def get_programs(self) -> List[Program]:
        """Return a list of all programs and their paths of the makefiles on the server

        Returns
        -------
        List[Program]
            A list of all programs with the paths of their makefiles.
        """
        return programs_by_makefiles(self.ssh)

    def get_cluster_info(self) -> ClusterInfo:
        """View partition and node information for the connected cluster.

        Returns
        -------
        List
            A list of lists which contain info about each partition of the cluster.
        """
        return slurm_info(self.ssh)

    def submit(self, config: Configuration) -> None:
        """Submit a configuration for analyzing a specified program with different tools.
        For each tool and each of their settings, the program is compiled accordingly
        and a jobscript is scheduled to run this specific setting of the tool.

        Parameters
        ----------
        config : Configuration
            The configuration object containing all information.
        """
        variables = Variables()
        run_pipeline(self.ssh, self.tools, config, variables, self.database_works)

    def get_all_jobs(self) -> List[AnalysisJob]:
        """Return a list of all jobs from the database.

        Returns
        -------
        List[AnalysisJob]
            The list of jobs.
        """
        return query_jobs(self.ssh)

    def upload_input_file(self, file_path: str) -> None:
        """Upload an input file onto the cluster.

        Parameters
        ----------
        file_path : str
            The file path on your device.
        """
        upload_input_file(self.ssh, file_path)

    def input_files(self) -> List[str]:
        """Return the list of all input file names.

        Returns
        -------
        List[str]
            A list of all input file names.
        """
        return input_files(self.ssh)

    def delete_input_file(self, file: str) -> None:
        """Delete an input file.

        Parameters
        ----------
        file : str
            The specified file name.
        """
        # TODO delete specified input file
        raise NotImplementedError

    def get_active_jobs(self):
        """Get all active jobs from the database.
        Args:
            ssh (SSH): The ssh connection.
        """
        if self.database_works:
            return query_jobs_by_status(self.ssh, SlurmJobStatus.Running)
        else:
            logging.info("Database does not work. Could not query active jobs.")
            return list()

    def get_jobs_by_tool(self, tool_name: str):
        """Get all jobs in the database which use a specfic tool.

        Args:
            ssh (SSH): The ssh connection.
            tool_name (str): The name of the tool.
        """
        if self.database_works:
            return query_jobs_by_tool(self.ssh, tool_name)
        else:
            logging.info("Database does not work. Could not query jobs by tool.")
            return list()

    def get_program_by_path(self, program_path: str) -> Program:
        """Return a program dataclass for a specified program path if it exists.

        Parameters
        ----------
        program_path : str
            The specified program path.

        Returns
        -------
        Program
            The program dataclass.
        """
        try:
            return _program_by_path(self.ssh, program_path)
        except FileNotFoundError as e:
            logging.error(e)
            return None

    def download_outputs(self, job_ids: List[str]) -> None:
        """Download the tool and job outputs for the specified job ids from the cluster onto your device.

        Parameters
        ----------
        job_ids : List[str]
            A list of job timestamp ids.
        """
        download_outputs(self.ssh, job_ids, self.database_works)
