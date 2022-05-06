from dataclasses import dataclass
from hpc_tools_framework.models import ListedEnvVar, SingleEnvVar
from datetime import datetime
from enum import Enum
from typing import List


class MailType(Enum):
    """The mail notification types."""

    NONE = 0
    BEGIN = 1
    """Job is started."""
    END = 2
    """Job finished successfully."""
    FAIL = 3
    """Job failed."""
    REQUEUE = 4
    ALL = 5
    """Equivalent to BEGIN, END, FAIL, REQUEUE, and STAGE_OUT."""
    STAGE_OUT = 6
    """Burst buffer stage out and teardown completed."""
    TIME_LIMIT = 7
    """Reached 100 percent of time limit."""
    TIME_LIMIT_90 = 8
    """Reached 90 percent of time limit."""
    TIME_LIMIT_80 = 9
    """Reached 80 percent of time limit."""
    TIME_LIMIT_50 = 10
    """Reached 50 percent of time limit."""
    ARRAY_TASKS = 11
    """Send emails for each array task."""


@dataclass
class Jobscript:
    """The jobscript class.
    See http://manpages.org/sbatch for details about the properties.
    """

    date: datetime
    """Timestamp of the creation of the jobscript."""
    name: str
    """Specify a name for the job allocation. The specified name will appear along with the job id number when querying running jobs on the system. The default is the name of the batch script, or just "sbatch" if the script is read on sbatch's standard input."""
    minnodes: int
    """Minimum number of nodes allocated to this job."""
    ntasks: int
    """sbatch does not launch tasks, it requests an allocation of resources and submits a batch script. This option advises the Slurm controller that job steps run within the allocation will launch a maximum of number tasks and to provide for sufficient resources. The default is one task per node, but note that the --cpus-per-task option will change this default."""
    partition: str
    """Request a specific partition for the resource allocation. If not specified, the default behavior is to allow the slurm controller to select the default partition as designated by the system administrator. If the job can use more than one partition, specify their names in a comma separate list and the one offering earliest initiation will be used with no regard given to the partition name ordering (although higher priority partitions will be considered first). When the job is initiated, the name of the partition used will be placed first in the job record partition string."""
    processes: int
    """The number of processes."""
    source: str
    """Source environment variable (for example needed in extrae; https://tools.bsc.es/sites/default/files/documentation/html/extrae/quick-guide.html#quick-running), only string because the name of the command must not be specified."""
    cp: str
    """The cp string."""
    executable_string: str
    """string of the executable inclusive all arguments as string and ./ start command."""
    single_env_variables: List[SingleEnvVar]
    """list of environment variables the tool needs in the jobscript (can be set in the shell but in this way it is more clear).
    Single variables are ones without a list multiple parameters, for example booleans.
    The list contains a tuple of name and value"""
    listed_env_variables: List[ListedEnvVar]
    """list of environment variables with multiple values (for example papi events),
    the list contains tuples of the environment variable name, a list of values and a seperator as a string"""
    pre_mpi_commands: List[str]
    """An ordered list of strings which are placed before the mpi command (mpi_exec, mpirun etc.) (most often empty)"""
    post_mpi_commands: List[str]
    """An ordered list of strings which are placed after the mpi command (mpi_exec, mpirun etc.) (binary of the tool, wrapper and flags )."""
    post_binary_flags: List[str]
    """An ordered list of strings which are placed after the executable."""
    memory: str
    """The allocated memory."""
    tool_name: str
    """The name of the analysis tool which is used for the program."""
    timeout: int = None
    """Set a limit on the total run time of the job allocation. If the requested time limit exceeds the partition's time limit, the job will be left in a PENDING state (possibly indefinitely). The default time limit is the partition's default time limit. When the time limit is reached, each task in each job step is sent SIGTERM followed by SIGKILL. The interval between signals is specified by the Slurm configuration parameter KillWait. The OverTimeLimit configuration parameter may permit the job to run longer than scheduled. Time resolution is one minute and second values are rounded up to the next minute.
    A time limit of zero requests that no time limit be imposed."""
    mail_user: str = None
    """User to receive email notification of state changes as defined by --mail-type. The default value is the submitting user."""
    mail_notifications: List[MailType] = None
    """Notify user by email when certain event types occur."""
    working_directory: str = None
    """Set the working directory of the batch script to directory before it is executed."""
    deadline: int = None
    """Remove the job if no ending is possible before this deadline."""
    cores_per_socket: int = None
    """Restrict node selection to nodes with at least the specified number of cores per socket."""
    checkpoint: int = None
    """Specifies the interval between creating checkpoints of the job step. By default, the job step will have no checkpoints created."""
    checkpoint_directory: str = None
    """Specifies the directory into which the job or job step's checkpoint should be written (used by the checkpoint/blcrm and checkpoint/xlch plugins only)"""
    no_kill: bool = False
    """Do not automatically terminate a job if one of the nodes it has been allocated fails. The user will assume the responsibilities for fault-tolerance should a node fail. When there is a node failure, any active job steps (usually MPI jobs) on that node will almost certainly suffer a fatal error, but with no_kill set to True, the job allocation will not be revoked so the user may launch new job steps on the remaining nodes in their allocation.
    By default Slurm terminates the entire job allocation if any node fails in its range of allocated nodes. """
    maxnodes: int = None
    """Optional maximum number of nodes allocated to this job. If it is not explicitly set, the maximum number of nodes is equal to the minimum."""
