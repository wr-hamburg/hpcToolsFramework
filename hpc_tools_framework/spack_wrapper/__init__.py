"""SPACK wrapper module."""

from hpc_tools_framework.spack_wrapper.spack_not_installed_exception import (
    SpackNotInstalledException,
)
from hpc_tools_framework.spack_wrapper.spack_initializer import init_spack
from hpc_tools_framework.spack_wrapper.tool_initializer import init_tool
from hpc_tools_framework.spack_wrapper.tool_info import tool_installation_dir

__all__ = [
    "SpackNotInstalledException",
    "init_spack",
    "init_tool",
    "tool_installation_dir",
]
