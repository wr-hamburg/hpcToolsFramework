from hpc_tools_framework.io import SSH, read_file
from hpc_tools_framework.constants import (
    JOBSCRIPT_OUTPUT_DIR,
    TOOL_DIR,
    OUTPUT_LOCAL_DIR,
)
from hpc_tools_framework.output_parser import Parser_format

import os


def parse_output(file: list[str], parser_format: Parser_format):
    """Parses the input file into a compilable Latex file and under the specifications of the parser format.

    Args:
        file (list[str]): The file to be parsed.
        parser_format (Parser_format): The format how the file should be parsed.

    Returns:
        list[str]: The body of a latex document as list of strings.
    """

    output_file = []
    for i, line in enumerate(file):
        if i in parser_format.format:
            if isinstance(parser_format.format[i][0], int):  # line break case
                line_breaks = parser_format.format[i]
                for j in line_breaks:
                    output_file.append(line[0:j])
                    line = line[j : len(line) - 1]
                output_file.append("\n")

            if type(parser_format.format[i][0]) == str:  # latex element case
                struct = parser_format.format[i]
                output_file.append("\\" + struct[0] + "{" + struct[1] + "}")
                output_file.append("\n")

        else:
            output_file.append(line)
    return output_file


def concat_latex(file, parser_format: Parser_format, job_id: int):
    """Concatinated the latex body with a footer and header which a read from the disk. Afterwards the file is saved to disk.

    Args:
        file (list[str]): The file to be parsed.
        parser_format (Parser_format): The format how the file should be parsed.
        job_id (int): The unique id of the job to name the latex file after.

    Returns:
        list[str]: A compileable latex file with header and footer.
    """
    header = open(".\\latex.header", "r")
    body = parse_output(file, parser_format)
    footer = open(".\\latex.footer", "r")

    latex_file = []

    for x in header:
        latex_file.append(x)
    latex_file.append("\n")
    for x in body:
        latex_file.append(x)
    latex_file.append("\n")
    latex_file.append(footer)

    with open(f"{job_id}.tex", "w") as f:
        for line in latex_file:
            f.write(line)

    return latex_file


def parse_jobscript_output(ssh: SSH, job_id: int):
    """Reads the output of a job and creates a PDF file for the output.

    Args:
        ssh (SSH): The SSH connection.
        job_id (int): The unique id of the job to name the latex file after.
    """
    jobscript_output = read_file(
        ssh, f"{TOOL_DIR}/{JOBSCRIPT_OUTPUT_DIR}/jobscript.{job_id}.out"
    )

    if not os.path.isdir(OUTPUT_LOCAL_DIR):
        os.makedirs(OUTPUT_LOCAL_DIR)
        concat_latex(
            jobscript_output, None, job_id
        )  # todo create parser format data class


# example,TODO delete soon

# o = Output_parser(
#     {
#         1: [3, 3, 2, 1, 1],
#         12: [1, 5, 11, 6],
#         17: [24],
#         15: ["section", "test"],
#         16: ["begin", "verbatim"],
#         17: ["end", "verbatim"],
#     }
# )
# f = []
# fi = open(".\\exampleFile.txt", "r")
# for x in fi:
#     f.append(x)

# concat_latex(f, o, 12)