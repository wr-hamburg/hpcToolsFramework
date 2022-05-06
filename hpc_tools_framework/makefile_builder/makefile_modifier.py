from typing import List
from hpc_tools_framework.models import ToolCompiler, CompilerLevel


def modify_makefile(
    makefile: List[str], tool_compiler: ToolCompiler = None
) -> List[str]:
    """Generate the makefile for the tool usage with the compiler parameters.

    Parameters
    ----------
    makefile : List[str]
        The makefile to modify.
    tool_compiler : ToolCompiler
        The compiler parameters. If nothing is provided, the original makefile is returned without any modifications.

    Returns
    -------
    List[str]
        The modified makefile.
    """
    if not tool_compiler:
        return makefile
    modified_makefile = list()
    for line in makefile:
        if line.startswith("CC"):
            if tool_compiler.compiler:
                line = f"CC = {tool_compiler.compiler}"
        if line.startswith("CFLAGS"):
            for level in CompilerLevel:
                line = line.replace("-" + level.value, "")
            if tool_compiler.compiler_level:
                line += f" -{tool_compiler.compiler_level} "
            else:
                # we use O2 as the default
                line += f" -{CompilerLevel.O2.value} "
            if tool_compiler.cflags:
                line += f"-{''.join(tool_compiler.cflags)} "
            if tool_compiler.include_link:
                line += f"-I {tool_compiler.include_link} "
            if tool_compiler.library_link:
                line += f"-L {tool_compiler.library_link}"
            # remove excess whitespace
            line = " ".join(line.split())
        if line.startswith("LIBS") and tool_compiler.libs:
            line += f" {''.join(tool_compiler.libs)}"
        modified_makefile.append(line)
    return modified_makefile
