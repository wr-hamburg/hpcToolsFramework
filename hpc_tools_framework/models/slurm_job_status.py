from enum import Enum


class SlurmJobStatus(Enum):
    """The Slurm job status."""

    Pending = 0
    """Job in inserted into the database and waiting to be scheduled with Slurm."""
    Queued = 1
    """Job is scheduled with Slurm and waiting to be started."""
    Running = 2
    """Job is running."""
    Finished = 3
    """Job is finished."""
    Failed = 4
    """Job execution failed."""
    Boot_Failed = 5
    Cancelled = 6
    Node_Fail = 7
    Out_Of_Memory = 8
    Suspended = 9
    Timeout = 10
    Requeue_Fed = 11
    Requeue_Hold = 12
    Requeue = 13
    Resizing = 14
    Stage_Out = 15
