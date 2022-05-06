from typing import List
from hpc_tools_framework.models import Jobscript, SlurmJobStatus
import time
from hpc_tools_framework.utils import url2dir, time_string
from hpc_tools_framework.constants import SCHEDULER_GIT_REPO, PYTHON_LOCAL


def generate(jobscript: Jobscript) -> List[str]:
    """Generates a jobscript file content which can be written in a file.

    Parameters
    ----------
    jobscript : Jobscript
        The jobscript object with all parameters.

    Returns
    -------
    List[str]
        The generated jobscript line by line.
    """
    blueprint = list()
    blueprint.append("#!/bin/sh")
    blueprint.append("")

    blueprint.append(f"## Creation date: {jobscript.date}")
    blueprint.append("")

    blueprint.append(f"#SBATCH --job-name={jobscript.name}")
    if jobscript.maxnodes:
        blueprint.append(
            f"#SBATCH --maxnodes={jobscript.minnodes}-{jobscript.maxnodes}"
        )
    else:
        blueprint.append(f"#SBATCH --nodes={jobscript.minnodes}")
    blueprint.append(f"#SBATCH --ntasks={jobscript.ntasks}")
    if jobscript.timeout:
        timeout = time.strftime("%d-%H:%M:%S".format(jobscript.timeout))
        blueprint.append(f"#SBATCH --time={timeout}")
    if jobscript.checkpoint and jobscript.checkpoint_directory:
        checkpoint = time.strftime("%d-%H:%M:%S".format(jobscript.checkpoint))
        blueprint.append(f"#SBATCH --checkpoint={checkpoint}")
        blueprint.append(f"#SBATCH --checkpoint-dir={jobscript.checkpoint_directory}")
    if jobscript.cores_per_socket:
        blueprint.append(f"#SBATCH --cores-per-socket={jobscript.cores_per_socket}")
    if jobscript.deadline:
        # TODO is this the correct format for: YYYY-MM-DD[THH:MM[:SS]]] ?
        deadline = time.strftime("%Y-%m-%d-%H:%M:%S".format(jobscript.deadline))
        blueprint.append(f"#SBATCH --deadline={deadline}")
    if jobscript.working_directory:
        blueprint.append(f"#SBATCH --workdir={jobscript.working_directory}")
    blueprint.append(f"#SBATCH --partition={jobscript.partition}")
    if jobscript.mail_user:
        blueprint.append(f"#SBATCH --mail-user={jobscript.mail_user}")
    if jobscript.mail_notifications:
        mail_notifications = [
            notification.name for notification in jobscript.mail_notifications
        ]
        blueprint.append(f"#SBATCH --mail-type={', '.join(mail_notifications)}")
    if jobscript.no_kill:
        blueprint.append("#SBATCH --no-kill")
    blueprint.append("")
    # TODO --mem-per-cpu, --mem and --mem-per-cpu are mutually exclusive
    # blueprint.append(f"#SBATCH --mem-per-cpu={jobscript.memory}")

    if jobscript.source:
        blueprint.append(f"source {jobscript.source}")
    if jobscript.cp:
        blueprint.append(f"cp {jobscript.cp}")
    # the output file name does not recognize directories
    # for this we change the directory from which we execute the jobscript in the scheduler
    blueprint.append(f"#SBATCH --output {jobscript.name}.out")
    blueprint.append(f"#SBATCH --error {jobscript.name}.err")
    blueprint.append("")

    for env in jobscript.single_env_variables:
        blueprint.append(f"export {env.name}={env.value}")
    blueprint.append("")
    for env in jobscript.listed_env_variables:
        env_listed = env.separator.join(env.values)
        blueprint.append(f"export {env.name} = {env_listed}")
    blueprint.append("")

    # init spack, activate local python env, load tool
    blueprint.append(". ../spack/share/spack/setup-env.sh")
   
    blueprint.append(f". ./../{PYTHON_LOCAL}/bin/activate")
    blueprint.append("spack load postgresql")
    blueprint.append(f"spack load {jobscript.tool_name}")


    blueprint.append(
        f"python ../{url2dir(SCHEDULER_GIT_REPO)}/job_status_updater.py {time_string(jobscript.date)} {SlurmJobStatus.Running.name}"
    )

    # TODO make mpi startup more dynamic (mpiexec..)
    executable_expression = ""
    if jobscript.pre_mpi_commands:
        executable_expression = " ".join(jobscript.pre_mpi_commands) + " "
    executable_expression += "mpirun "
    if jobscript.processes:
        executable_expression += f"-np {jobscript.processes} "
    if jobscript.post_mpi_commands:
        executable_expression += " ".join(jobscript.post_mpi_commands) + " "
    executable_expression += jobscript.executable_string + " "
    if jobscript.post_binary_flags:
        executable_expression += " ".join(jobscript.post_binary_flags)
    executable_expression = executable_expression.rstrip()
    blueprint.append(executable_expression)

    blueprint.append(
        f"python ../{url2dir(SCHEDULER_GIT_REPO)}/job_status_update.py {time_string(jobscript.date)} {SlurmJobStatus.Finished.name}"
    )

    return blueprint
