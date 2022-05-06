from hpc_tools_framework.io import SSH
from hpc_tools_framework.models import ToolOutput, OutputType
from hpc_tools_framework.output_parser import (
    parse_jobscript_output,
)


def parse_outputs(ssh: SSH, tool_output: ToolOutput, job_id: int):

    if tool_output.type == OutputType.Jobscript_Output:
        parse_jobscript_output(ssh, job_id)
