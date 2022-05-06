from datetime import datetime, timezone
import logging
from time import sleep
from typing import List
from hpc_tools_framework.io import SSH
from hpc_tools_framework.utils import (
    single_or_default,
    time_string,
    extend_or_overwrite,
    Variables,
)
from hpc_tools_framework.models import (
    Configuration,
    SettingType,
    SingleEnvVar,
    ListedEnvVar,
    Tool,
    AnalysisJob,
    SlurmJobStatus,
)
from hpc_tools_framework.constants import (
    OUTPUT_DIR,
    JOBSCRIPT_DIR,
    TOOL_DIR,
    JOBSCRIPT_OUTPUT_DIR,
)
from hpc_tools_framework.makefile_builder import create_makefile
from hpc_tools_framework.job_builder import build_jobscripts, create_jobscript
from hpc_tools_framework.spack_wrapper import init_tool
from hpc_tools_framework.core.system_info import system_cpu
from hpc_tools_framework.scheduler import insert_job


def run_pipeline(
    ssh: SSH,
    tools: List[Tool],
    config: Configuration,
    variables: Variables,
    database_works: bool,
) -> None:
    """Executes the pipeline. It creates a Makefile and Jobscript for each Analysis job.
    And pushes the Analysis job into the database.

    Parameters
    ----------
    ssh : SSH
        The ssh connection to the cluster.
    tools : List[Tool]
        The list of tools.
    config : Configuration
        The configuration of all analysis jobs.
    variables : Variables
        The variables.
    database_works : bool
        Tells whether the database works and a job can be inserted.
    """

    for selected_tool in config.tools:
        tool = single_or_default(tools, "name", selected_tool.name)
        for sel_setting in selected_tool.settings:
            timestamp = datetime.now()
            setting = single_or_default(tool.settings, "name", sel_setting.name)
            timestamp_id = time_string(timestamp)
            variables.set_output(f"../{OUTPUT_DIR}/" + timestamp_id)
            variables.set_cpu(system_cpu(ssh))
            tool_installation = extend_or_overwrite(
                tool.installation, setting.installation
            )
            installation_dir = init_tool(ssh, tool.name, tool_installation)
            variables.set_home(installation_dir)
            logging.info(f"{tool.name} initialized.")

            # generate makefile
            tool_compiler = extend_or_overwrite(tool.compiler, setting.compiler)
            makefile_path = create_makefile(
                ssh=ssh,
                makefile_path=config.program_config.program.makefile_path,
                timestamp=timestamp,
                tool_compiler=tool_compiler,
                variables=variables,
            )

            tool_job = extend_or_overwrite(tool.job, setting.job)
            # extend tool job with user selected setting parameters
            if sel_setting.type == SettingType.Bool:
                pass
            elif (
                sel_setting.type == SettingType.Textinput
                or sel_setting.type == SettingType.Numberinput
            ):
                tool_job.single_env_variables.append(
                    SingleEnvVar(name=sel_setting.name, value=sel_setting.values)
                )
                variables.set_input(sel_setting.values)
            elif sel_setting.type == SettingType.Set:
                tool_job.listed_env_variables.append(
                    ListedEnvVar(
                        name=sel_setting.name,
                        values=sel_setting.values,
                        separator=sel_setting.separator,
                    )
                )
                variables.set_set(sel_setting.values)
            elif sel_setting.type == SettingType.File:
                # TODO setting type file
                pass

            jobscript = build_jobscripts(
                job=tool_job,
                job_config=config.job_config,
                timestamp=timestamp,
                tool_config=selected_tool,
                program_config=config.program_config,
            )
            create_jobscript(ssh=ssh, jobscript=jobscript, variables=variables)

            analysis_job = AnalysisJob(
                id=None,
                timestamp_id=timestamp_id,
                status=SlurmJobStatus.Pending,
                program_name=config.program_config.program.name,
                job_config=config.job_config,
                tool_config=selected_tool,
                makefile_path=makefile_path,
                jobscript_path=f"{TOOL_DIR}/{JOBSCRIPT_DIR}/{jobscript.name}",
                jobscript_ouput_path=f"{TOOL_DIR}/{JOBSCRIPT_OUTPUT_DIR}/{jobscript.name}.out",
                jobscript_ouput_error_path=f"{TOOL_DIR}/{JOBSCRIPT_OUTPUT_DIR}/{jobscript.name}.err",
                tool_output_path=f"{TOOL_DIR}/{OUTPUT_DIR}/{timestamp_id}",
                created=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                scheduled_time=None,
                started_time=None,
                finished_time=None,
            )
            if database_works:
                insert_job(ssh, analysis_job)
            else:
                logging.info(
                    "Because the database does not work, no job was inserted into it."
                )

            # check that some time passed so that the next timestamp is different
            new_timestamp = datetime.now()
            time_difference = new_timestamp - timestamp
            if time_difference.microseconds == 0:
                sleep(0.000001)